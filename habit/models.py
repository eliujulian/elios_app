import datetime
from django.utils import timezone
from django.db import models
from django.shortcuts import reverse
from core.models import AbstractBaseModel, User
from core.definitions import *


class HabitProfile(AbstractBaseModel):
    profile_for = models.OneToOneField(to=User, on_delete=models.CASCADE, editable=False)

    # Visions
    vision_1 = models.TextField(null=True, blank=True)
    vision_2 = models.TextField(null=True, blank=True)
    vision_3 = models.TextField(null=True, blank=True)
    vision_4 = models.TextField(null=True, blank=True)
    vision_5 = models.TextField(null=True, blank=True)
    vision_6 = models.TextField(null=True, blank=True)
    vision_7 = models.TextField(null=True, blank=True)
    vision_8 = models.TextField(null=True, blank=True)

    LABELS = {
        'vision_1': 'Arbeit',
        'vision_2': 'Finanzen',
        'vision_3': 'Gesundheit',
        'vision_4': 'Freizeit und Interessen',
        'vision_5': 'Beziehung und Liebe',
        'vision_6': 'Familie und Kinder',
        'vision_7': 'Geselligkeit und Freunde',
        'vision_8': 'Persönlichkeit'
    }

    def get_visions(self):
        return [
            (1, self.LABELS['vision_1'], self.vision_1),
            (2, self.LABELS['vision_2'], self.vision_2),
            (3, self.LABELS['vision_3'], self.vision_3),
            (4, self.LABELS['vision_4'], self.vision_4),
            (5, self.LABELS['vision_5'], self.vision_5),
            (6, self.LABELS['vision_6'], self.vision_6),
            (7, self.LABELS['vision_7'], self.vision_7),
            (8, self.LABELS['vision_8'], self.vision_8)
        ]

    def get_absolute_url(self):
        return reverse("habitprofile")

    def get_all_habits(self):
        return Habit.objects.filter(created_by_id=self.created_by_id, is_active=True)

    def get_habits(self, date: datetime.date):
        habits = Habit.objects.filter(created_by_id=self.created_by_id, is_active=True)
        daily_habits = habits.filter(interval=1)
        if date.isoweekday() >= 6:
            daily_habits = daily_habits.filter(skip_weekend=False)
        else:
            daily_habits = daily_habits.filter(skip_weekdays=False)

        weekly_habits = habits.filter(interval=2, day_of_week=date.isoweekday())
        monthly_habits = habits.filter(interval=3)
        if 1 <= date.day <= 3 or date.day == 15:
            monthly_habits = monthly_habits.filter(day_of_month=date.day)
            return daily_habits | weekly_habits | monthly_habits

        return daily_habits | weekly_habits

    def get_habits_today(self):
        return self.get_habits(datetime.date.today())

    def get_habits_yesterday(self):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        habits = self.get_habits(yesterday)
        habits = habits.filter(last_day__lt=yesterday)
        return habits

    def yesterday_open_items(self):
        return bool(self.get_habits_yesterday().count())

    def __str__(self):
        return f"HabitProfile for {self.profile_for}"


class Goal(AbstractBaseModel):
    class Meta:
        ordering = ['sphere', 'title']
    id_slug = models.CharField(max_length=18, unique=True, editable=False)
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True, null=True)
    sphere = models.IntegerField(choices=SPHERE_OF_LIFE_DE, default=1)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("goal-detail", args=[self.id_slug, ])

    def get_create_url(self):
        return reverse("goal-create")

    def __str__(self):
        return f"{self.title}"


class Habit(AbstractBaseModel):
    class Meta:
        ordering = ['sphere', 'title']

    INTERVAL = (
        (1, 'täglich'),
        (2, 'wöchentlich'),
        (3, 'monatlich')
    )

    DAYS = (
        (1, 'Montag'),
        (2, 'Dienstag'),
        (3, 'Mittwoch'),
        (4, 'Donnerstag'),
        (5, 'Freitag'),
        (6, 'Samstag'),
        (7, 'Sonntag')
    )

    DAY_OF_MONTH = (
        (1, 'Erster Tag'),
        (2, 'Zweiter Tag'),
        (3, 'Dritter Tag'),
        (15, 'Monatsmitte (15.)'),
        (-3, 'Letzter Sonntag im Monat'),
        (-2, 'Vorletzter Tag'),
        (-1, 'Letzter Tag')
    )

    HABIT_ACTION = (
        (1, 'done'),
        (2, 'failed'),
        (3, 'canceled')
    )

    def get_choices(self):
        return {'created_by': self.created_by}

    id_slug = models.CharField(max_length=18, unique=True, editable=False)
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True, null=True)
    sphere = models.IntegerField(choices=SPHERE_OF_LIFE_DE, default=1)
    is_active = models.BooleanField(default=True)
    is_good_habit = models.BooleanField(default=True)
    goal = models.ForeignKey(to=Goal, on_delete=models.SET_NULL,
                             # limit_choices_to=get_choices,
                             null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    # Interval
    interval = models.IntegerField(choices=INTERVAL, default=1)
    skip_weekend = models.BooleanField(default=False)
    skip_weekdays = models.BooleanField(default=False)
    day_of_week = models.IntegerField(choices=DAYS, default=1)
    day_of_month = models.IntegerField(choices=DAY_OF_MONTH, default=1)

    # Stats
    current_streak = models.IntegerField(default=0, editable=False)
    highest_streak = models.IntegerField(default=0, editable=False)
    total_done = models.IntegerField(default=0, editable=False)
    total_failed = models.IntegerField(default=0, editable=False)
    total_canceled = models.IntegerField(default=0, editable=False)
    total_counter = models.IntegerField(default=0, editable=False)
    last_day = models.DateField(null=True, blank=True, editable=False)
    last_day_action = models.IntegerField(choices=HABIT_ACTION, null=True, blank=True, editable=False)

    # Privacy - Sharing with other users
    privacy = models.IntegerField(choices=PRIVACY_OPTIONS, default=PRIVACY_OPTIONS[0][0])

    def get_direction(self):
        if self.is_good_habit:
            return "gute Gewohnheit"
        else:
            return "schlechte Gewohnheit"

    def serialize(self):
        return {
            'id_slug': self.id_slug,
            'title': self.title,
            'description': self.description,
            'sphere': self.sphere,
            'is_active': self.is_active,
            'is_good_habit': self.is_good_habit,
            'link': self.link,
            'current_streak': self.current_streak,
            'last_day': self.last_day,
            'last_day_action': self.last_day_action,
        }

    def open_today(self):
        today = timezone.now().date()
        if self.last_day < today:
            return True
        else:
            return False

    def open_yesterday(self):
        today = timezone.now().date()
        yesterday = today - datetime.timedelta(days=1)
        if self.last_day < yesterday:
            return True
        else:
            return False

    def get_create_url(self):
        return reverse("habit-create")

    def get_absolute_url(self):
        return reverse("habit-detail", args=[self.id_slug, ])

    def create_event(self, date, status):
        instance = HabitEvent.objects.create(
            **{'created_by': self.created_by,
               'timestamp_created': timezone.now(),
               'timestamp_changed': timezone.now(),
               'id_slug': Habit.get_id_slug(10),
               'habit': self,
               'title': self.title,
               'sphere': self.sphere,
               'status': status,
               'date': date
               }
        )
        return instance

    def _change_status(self, date, status: int):
        assert status in [1, 2, 3]
        assert isinstance(date, datetime.date)
        if not self.last_day or date > self.last_day:
            self.last_day = date
            self.last_day_action = status
            self.create_event(date, status)
        else:
            raise Exception("Date has to be higher than last_day.")

    def mark_as_done(self, date):
        self._change_status(date, 1)
        self.current_streak += 1
        if self.current_streak > self.highest_streak:
            self.highest_streak = self.current_streak
        self.total_done += 1
        self.total_counter += 1
        self.save()
    
    def mark_as_failed(self, date):
        self._change_status(date, 2)
        self.total_failed += 1
        self.current_streak = 0
        self.total_counter += 1
        self.save()

    def mark_as_canceled(self, date):
        self._change_status(date, 3)
        self.total_canceled += 1
        self.save()

    def __str__(self):
        return f"{self.title} ({self.get_sphere_display()})"


class HabitEvent(AbstractBaseModel):
    id_slug = models.CharField(max_length=18, unique=True, editable=False)
    habit = models.ForeignKey(Habit, models.CASCADE)
    title = models.CharField(max_length=160)
    sphere = models.IntegerField(choices=SPHERE_OF_LIFE_DE)
    status = models.IntegerField(choices=Habit.HABIT_ACTION)
    date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.date} - {self.get_status_display()}"
