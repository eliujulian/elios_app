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

    def get_absolute_url(self):
        return reverse("habit")

    def __str__(self):
        return f"HabitProfile for {self.profile_for}"


class Goal(AbstractBaseModel):
    class Meta:
        abstract = True

    title = models.CharField(max_length=160)
    description = models.TextField(blank=True, null=True)
    sphere = models.IntegerField(choices=SPHERE_OF_LIFE_DE, default=1)

    def __str__(self):
        return self.title


class Habit(AbstractBaseModel):
    class Meta:
        abstract = True

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
        (30, 'Vorletzter Tag'),
        (31, 'Letzter Tag')
    )

    title = models.CharField(max_length=160)
    description = models.TextField(blank=True, null=True)
    sphere = models.IntegerField(choices=SPHERE_OF_LIFE_DE, default=1)
    is_active = models.BooleanField(default=True)
    goal = models.ForeignKey(to=Goal, on_delete=models.SET_NULL, null=True, blank=True)
    interval = models.IntegerField(choices=INTERVAL, default=1)
    skip_weekend = models.BooleanField(default=False)
    skip_weekdays = models.BooleanField(default=False)
    day_of_week = models.IntegerField(choices=DAYS, default=1)
    day_of_month = models.IntegerField(choices=DAY_OF_MONTH, default=1)
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title
