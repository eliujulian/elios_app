from django.forms import ModelForm
from health.models import *


class WeightForm(ModelForm):
    class Meta:
        model = Weight
        fields = [
            "measurement_date",
            "weight"
        ]
        labels = {
            "measurement_date": "Datum",
            "weight": "Gewicht"
        }