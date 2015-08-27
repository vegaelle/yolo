from calendar import Calendar
from datetime import timedelta, date, datetime
import copy

from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.text import slugify
from polymorphic import PolymorphicModel
from dateutils import relativedelta

from .validators import colorValidator


class EventDay:

    def __init__(self, day, attributes=None):
        if isinstance(day, date):
            self.date = day
        elif isinstance(day, datetime):
            self.date = day.date
        self.events = []
        if attributes is None:
            attributes = {}
        self.attributes = attributes

    def add_attributes(self, attributes):
        self.attributes.update(attributes)

    def append(self, item):
        self.events.append(item)

    def __len__(self):
        return len(self.events)

    def __iter__(self):
        return self.events.__iter__()

    def __str__(self):
        return '{count} item{s} for {date}'\
            .format(count=len(self.events),
                    s='s' if len(self.events) > 1 else '',
                    date=self.date.strftime('%m/%d/%Y'))

    def __repr__(self):
        return self.__str__()


class EventView:

    def __init__(self, events, date_getter, end_getter=None, days=None):
        self.events = events
        self.date_getter = date_getter
        self.end_getter = end_getter
        # self.days = defaultdict(lambda: EventDay())
        self.days = {}
        if days is not None:
            self.add_days_attributes(days)
        self.add_events(events)

    def add_events(self, events, date_getter=None, end_getter=None):
        """
        adds a list of events to an EventView. Events should be a list of
        objects. Date_getter and end_getter should be attribute/key names of
        Date objects in the events, or callables that return date objects.
        """
        if date_getter is None:
            date_getter = self.date_getter
        if end_getter is None:
            end_getter = self.end_getter

        for event in events:
            self.add_event(event, date_getter, end_getter)

    def add_event(self, event, date_getter, end_getter=None):
        """
        adds an event to an EventView. It can be any kind of object.
        Date_getter and end_getter should be attribute/key names of
        Date objects in the event, or callables that return date object.
        """
        event_date = self.get_date_info(event, date_getter)
        if event_date not in self.days:
            self.days[event_date] = EventDay(event_date)
        if end_getter is not None:
            event_end = self.get_date_info(event, end_getter)
        if event_end > event_date:
            end_date = event_end
            cur_tmp_date = event_date
            while cur_tmp_date <= end_date:
                if cur_tmp_date not in self.days:
                    default_attributes = {
                        'active': False,
                        'today': cur_tmp_date == date.today(),
                    }
                    self.days[cur_tmp_date] = EventDay(
                        cur_tmp_date,
                        attributes=default_attributes)
                self.days[cur_tmp_date].append(event)
                cur_tmp_date = cur_tmp_date + timedelta(days=1)
        else:
            self.days[event_date].append(event)

    def add_days_attributes(self, days):
        """
        adds attributes to a day object.
        The 'days' argument must be a dict, in which keys are date objects,
        and values are dicts of attributes.
        """
        for day, attributes in days.items():
            if day in self.days:
                self.days[day].add_attributes(attributes)
            else:
                self.days[day] = EventDay(day, attributes)

    def get_date_info(self, event, getter):
        """
        Returns the date or the duration of an event object, given by the
        getter parameter. This may be callable, taking the event in parameter,
        and returning a Date/Timedelta object, or may be  key of a dict, or
        attribute.
        """
        if callable(getter):
            value = getter(event)
        else:
            try:
                value = getattr(event, getter)
            except AttributeError:
                try:
                    value = event[getter]
                except TypeError:
                    raise TypeError('getter could not apply to event')

        if isinstance(value, datetime):
            value = value.date
        elif isinstance(value, date):
            pass
        else:
            raise ValueError('{} should be a date'.format(value))
        return value

    def calendar(self):
        """
        Renders the view as a list of months.
        """
        if len(self.days) == 0:
            raise ValueError('Calendar rendering is not permitted without '
                             'events.')
        cal = Calendar()
        months = []
        remaining_days = sorted([k for k in self.days.keys()])
        current_day = remaining_days[0].replace(day=1)
        remaining_events = len(self.events)
        while remaining_events > 0:
            month = cal.monthdatescalendar(current_day.year, current_day.month)
            month_view = []
            for i, month_week in enumerate(month):
                month_view.append([])
                for j, day in enumerate(month_week):
                    if day.weekday() not in [5, 6]:  # weekend removal
                        month_view[i].append([])
                        if day in self.days:
                            events, daily_events_count = \
                                self._extract_day_events(day)
                            events = copy.deepcopy(events)
                            events.add_attributes({
                                'cur_month': day.month == current_day.month,
                            })
                            remaining_events -= daily_events_count
                            month_view[i][j] = events
                        else:

                            default_attributes = {
                                'active': False,
                                'today': day == date.today(),
                                'cur_month': day.month == current_day.month
                            }
                            month_view[i][j] = EventDay(
                                day,
                                attributes=default_attributes)
            months.append({'month': current_day,
                           'dates': month_view})
            current_day = current_day + relativedelta(months=1)
        return months

    def _extract_day_events(self, day):
        events = self.days[day]
        # removing to counter the already-removed events
        daily_events_count = 0
        for i, ev in enumerate(events):
            if self.get_date_info(ev, self.date_getter) == \
                    events.date:
                daily_events_count += 1
        return (events, daily_events_count)


def get_event_calendar(year, month, events=[]):
    c = Calendar()
    cal = c.monthdatescalendar(year, month)
    # replacing Date objects with tuples
    for i, w in enumerate(cal):
        for j, d in enumerate(w):
            cal[i][j] = (d, [])

    return cal


class Member(models.Model):
    user = models.OneToOneField(User, verbose_name='utilisateur',
                                related_name='member')
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True)
    type = models.CharField(max_length=10, choices=(('student', 'élève'),
                                                    ('teacher', 'formateur'),
                                                    ('admin', 'administrateur')
                                                    ),
                            verbose_name='type')
    tags = models.ManyToManyField('Tag', related_name='members',
                                  verbose_name='tags', blank=True)

    def __str__(self):
        return self.user.__str__()

    class Meta:
        verbose_name = 'Membre'


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='nom', unique=True)
    color = models.CharField(max_length=7, verbose_name='couleur',
                             validators=[colorValidator])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'tag'

    def to_css(self):
        """
        Returns the slugged name, for CSS class integration
        """
        return slugify(self.name)


# Resource models


class Formation(models.Model):
    name = models.CharField(max_length=50, verbose_name='nom', unique=True)
    description = models.TextField(verbose_name='description', blank=True)
    days_count = models.PositiveIntegerField(verbose_name='nombre de jours')
    objectives = models.ManyToManyField('Objective', verbose_name='objectifs',
                                        related_name='formations')
    tags = models.ManyToManyField('Tag', verbose_name='tags',
                                  related_name='formations')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'formation'


class Objective(models.Model):
    name = models.CharField(max_length=50, verbose_name='nom', unique=True)
    points = models.PositiveIntegerField(verbose_name='nombre de points')
    description = models.TextField(verbose_name='description', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'objectif'


class Course(PolymorphicModel):
    name = models.CharField(max_length=50, verbose_name='nom', unique=True)
    description = models.TextField(verbose_name='description', blank=True)
    standard_duration = models.DurationField(verbose_name='durée standard',
                                             default=timedelta(days=1))
    dependencies = models.ManyToManyField('Objective',
                                          verbose_name='dépendances',
                                          related_name='dependant_courses',
                                          blank=True)
    objectives = models.ManyToManyField('Objective',
                                        verbose_name='objectifs apportés',
                                        related_name='courses',
                                        blank=True)
    tag = models.ForeignKey('Tag', verbose_name='tag', related_name='courses')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'cours'
        verbose_name_plural = 'cours'


class LectureCourse(Course):
    content = models.TextField(verbose_name='contenu')

    class Meta:
        verbose_name = 'cours théorique'


class LectureFile(models.Model):
    course = models.ForeignKey('LectureCourse', verbose_name='cours',
                               related_name='files')
    file = models.FileField(upload_to='lectures')
    type = models.CharField(max_length=50, verbose_name='type MIME de fichier')

    def save(self, *args, **kwargs):
        """
        fetching filetype
        """
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'support de cours'
        verbose_name_plural = 'supports de cours'


class QuestionCourse(Course):

    class Meta:
        verbose_name = 'questionnaire'


class Question(models.Model):
    course = models.ForeignKey('QuestionCourse', verbose_name='questionnaire',
                               related_name='questions')
    label = models.CharField(max_length=50, verbose_name='intitulé')
    order = models.PositiveIntegerField(verbose_name='ordre')
    question_type = models.CharField(max_length=10,
                                     choices=(('mono', 'une seule réponse'),
                                              ('multi', 'plusieurs réponses'),
                                              ),
                                     verbose_name='type de question')

    def __str__(self):
        return '{course} : {question}'.format(course=self.course.name,
                                              question=self.label)

    class Meta:
        verbose_name = 'question'
        unique_together = (('course', 'order'), )


class Answer(models.Model):
    question = models.ForeignKey('Question')
    label = models.CharField(max_length=50, verbose_name='réponse')
    order = models.PositiveIntegerField(verbose_name='ordre')
    valid = models.BooleanField(verbose_name='réponse vraie', default=False)

    def __str__(self):
        return '{question} — {answer}'.format(question=self.question.__str__(),
                                              answer=self.label)

    class Meta:
        verbose_name = 'réponse'
        unique_together = (('question', 'order'), )


class PracticeCourse(Course):
    instructions = models.TextField(verbose_name='instructions')
    repository = models.URLField(verbose_name='dépôt')

    class Meta:
        verbose_name = 'cours pratique'


# Calendar attribution models

class Promotion(models.Model):
    name = models.CharField(max_length=50, verbose_name='promotion',
                            unique=True)
    group = models.OneToOneField(Group, verbose_name='groupe',
                                 related_name='promotion')
    image = models.ImageField(upload_to='promotion', verbose_name='avatar de '
                              'la promotion')
    formation_type = models.ForeignKey('Formation', verbose_name='type de '
                                       'formation', related_name='promotions')

    def __str__(self):
        return self.name

    def calendars(self):
        """ returns a list of Calendar objects (list of weeks, represented by
        DateTime/lists of events tuples) with all events for the current
        Promotion.
        """
        ev = EventView(self.courses.all(), lambda c: c.begin.date(),
                       lambda c: c.end.date())
        attributes = {day.day: day.attributes() for day in self.days.all()}
        ev.add_days_attributes(attributes)
        return ev.calendar()

    class Meta:
        verbose_name = 'promotion'


class DayAttribution(models.Model):
    promotion = models.ForeignKey('Promotion', verbose_name='promotion',
                                  related_name='days')
    assigned = models.ForeignKey('Member', verbose_name='formateur',
                                 related_name='days')
    day = models.DateField(verbose_name='jour')
    tag = models.ForeignKey('Tag', verbose_name='tag', related_name='days')

    def attributes(self):
        """
        Returns a dict of attributes for the current day.
        """
        attrs = {}
        attrs['active'] = True
        attrs['today'] = self.day == date.today()
        attrs['assigned'] = self.assigned
        attrs['tag'] = self.tag
        return attrs

    def __str__(self):
        return '{promotion} : {day}'.format(promotion=self.promotion.name,
                                            day=self.day)

    class Meta:
        verbose_name = 'attribution de jour'
        verbose_name_plural = 'attributions de jours'


class ObjectiveAttribution(models.Model):
    promotion = models.ForeignKey('Promotion', verbose_name='promotion',
                                  related_name='objectives')
    objective = models.ForeignKey('Objective', verbose_name='objectif',
                                  related_name='attributed_courses')
    day = models.DateField(verbose_name='jour')

    def __str__(self):
        return '{promotion} — {objective}'.\
            format(promotion=self.promotion.name,
                   objective=self.objective.name)

    class Meta:
        verbose_name = 'attribution d’objectif'
        verbose_name_plural = 'attributions d’objectifs'
        unique_together = (('promotion', 'objective'), )


class CourseAttribution(models.Model):
    promotion = models.ForeignKey('Promotion', verbose_name='promotion',
                                  related_name='courses')
    course = models.ForeignKey('Course', verbose_name='cours',
                               related_name='course_attributions')

    begin = models.DateTimeField(verbose_name='date et heure de début')
    end = models.DateTimeField(verbose_name='date et heure de fin')

    def __str__(self):
        return '{promotion} — {course}'.format(promotion=self.promotion.name,
                                               course=self.course.name)

    class Meta:
        verbose_name = 'attribution de cours'
        verbose_name_plural = 'attributions de cours'
        unique_together = (('promotion', 'course'), )
