from datetime import timedelta, date, datetime
from calendar import Calendar
import copy

from dateutils import relativedelta


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
