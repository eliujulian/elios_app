from django.db import models
from django.shortcuts import reverse
from core.models import AbstractNoteModel, AbstractBaseModel, User
from core.definitions import FIVE_SCALA


class PersonalityProfile(AbstractBaseModel):
    """
    Big 5
    1. Openness, Offenheit für Neues
    2. Gewissenhaftigkeit / Perfektionismus
    3. Geselligkeit
    4. Rücksichtnahme, Kooperationsbereitschaft, Empathie
    5. Neurotizismus, Emotionale Labilität, Verletzlichkeit
    """
    profile_about = models.OneToOneField(to=User, on_delete=models.CASCADE, editable=False)
    open_minded_score = models.IntegerField(choices=FIVE_SCALA, default=3)
    conscientiousness_score = models.IntegerField(choices=FIVE_SCALA, default=3)
    extraversion_score = models.IntegerField(choices=FIVE_SCALA, default=3)
    agreeableness_score = models.IntegerField(choices=FIVE_SCALA, default=3)
    neuroticism_score = models.IntegerField(choices=FIVE_SCALA, default=3)

    def open_minded_range(self):
        return range(0, self.open_minded_score)

    def conscientiousness_range(self):
        return range(0, self.conscientiousness_score)

    def extraversion_range(self):
        return range(0, self.extraversion_score)

    def agreeableness_range(self):
        return range(0, self.agreeableness_score)

    def neuroticism_range(self):
        return range(0, self.neuroticism_score)

    def get_absolute_url(self):
        return reverse("personality")

    def notes(self):
        return self.personalitynote_set.all()

    def __str__(self):
        return str(self.profile_about)


class PersonalityNote(AbstractNoteModel):
    note_about = models.ForeignKey(to=PersonalityProfile, on_delete=models.CASCADE, editable=False)
    id_slug = models.CharField(max_length=18, unique=True, editable=False)

    def get_absolute_url(self):
        return reverse("personality")

    def get_update_url(self):
        return reverse("personality-note-update", args=[self.id_slug, ])

    def get_create_url(self):
        return reverse("personality-note-create")

    def get_delete_url(self):
        return reverse("personality-note-delete", args=[self.id_slug, ])

    def __str__(self):
        return self.title


class Journal(AbstractBaseModel):
    class Meta:
        abstract = True

    id_slug = models.CharField(max_length=18, unique=True, editable=False)
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class JournalEntry(AbstractBaseModel):
    class Meta:
        abstract = True

    def get_choices(self):
        return {'created_by': self.created_by}

    id_slug = models.CharField(max_length=18, unique=True, editable=False)
    date = models.DateField()
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True, null=True)
    journal = models.ForeignKey(Journal, models.SET_NULL, limit_choices_to=get_choices)

    def __str__(self):
        return f"{self.date} - {self.title}"
