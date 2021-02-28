from django.forms import ModelForm
from habit.models import *


class HabitProfileForm(ModelForm):
    class Meta:
        model = HabitProfile
        fields = '__all__'


class GoalForm(ModelForm):
    class Meta:
        model = Goal
        fields = [
            'sphere',
            'title',
            'description',
            'is_active'
        ]
        labels = {
            'sphere': 'Bereich',
            'title': 'Titel',
            'description': 'Beschreibung',
            'is_active': 'Aktiv'
        }


class HabitForm(ModelForm):
    class Meta:
        model = Habit
        fields = '__all__'
