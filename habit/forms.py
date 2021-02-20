from django.forms import ModelForm
from habit.models import *


class HabitProfileForm(ModelForm):
    class Meta:
        model = HabitProfile
        fields = '__all__'

