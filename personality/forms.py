from django.forms import ModelForm
from personality.models import PersonalityProfile


class PersonalityUpdateForm(ModelForm):
    class Meta:
        model = PersonalityProfile
        fields = [
            'open_minded_score',
            'conscientiousness_score',
            'extraversion_score',
            'agreeableness_score',
            'neuroticism_score'
        ]
