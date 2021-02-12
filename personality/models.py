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
    profile_about = models.OneToOneField(to=User, on_delete=models.CASCADE)
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

    def __str__(self):
        return str(self.profile_about)
