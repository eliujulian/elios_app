import datetime
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from core.models import AbstractBaseModel


class Weight(AbstractBaseModel):
    class Meta:
        ordering = ['-measurement_date']

    measurement_date = models.DateField()
    weight = models.FloatField()

    @property
    def measurement_date_str(self):
        return self.measurement_date.strftime("%d.%m.%Y")

    @property
    def weight_5char(self):
        return " " * (5 - len(str(self.weight))) + str(self.weight)

    def current_weight(self):
        return Weight.objects.filter(user=self.created_by)[0].weight

    def last_measure(self):
        instance = Weight.objects.filter(user=self.created_by)[0]
        return instance.measurement_date

    def max_weight(self):
        return max([n.weight for n in Weight.objects.filter(user=self.created_by)])

    def min_weight(self):
        return min([n.weight for n in Weight.objects.filter(user=self.created_by)])

    def average_weight(self):
        weights = Weight.objects.filter(user=self.created_by)
        return round(sum([n.weight for n in weights]) / weights.count(), 1)

    def average_weight_one_year(self):
        data = Weight.objects.filter(user=self.created_by,
                                     measurement_date__gt=datetime.date(timezone.now().year - 1,
                                                                        timezone.now().month,
                                                                        timezone.now().day))
        return round(sum([n.weight for n in data]) / data.count(), 1)

    def get_absolute_url(self):
        return reverse("health-weight-detail", kwargs={"pk": self.id})

    def get_update_url(self):
        return reverse("health-weight-update", kwargs={"pk": self.id})

    def __str__(self):
        return str(self.measurement_date.strftime("%d.%m.%Y")) + ": " + str(self.weight)
