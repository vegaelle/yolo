from datetime import timedelta, date

from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.utils.text import slugify
from polymorphic import PolymorphicModel

from .validators import colorValidator
from .eventview import EventView


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

    def is_owned(self, user, perm):
        if perm == 'learning.view_course':
            try:
                attribution = self.course_attributions.get(
                    promotion__group__in=user.groups.all())
                return attribution.begin < timezone.now()
            except CourseAttribution.DoesNotExist:
                return False
        return True

    class Meta:
        verbose_name = 'cours'
        verbose_name_plural = 'cours'
        permissions = (('view_course', 'Can view a course'), )


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
