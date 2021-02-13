from django.forms import ModelForm
from personality.models import PersonalityProfile, PersonalityNote


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


class NoteForm(ModelForm):
    class Meta:
        model = PersonalityNote
        fields = [
            'title',
            'sphere',
            'description'
        ]
        labels = {
            'title': 'Titel',
            'sphere': 'Bereich',
            'description': 'Beschreibung'
        }
