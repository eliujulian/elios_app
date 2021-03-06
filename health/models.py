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
        return Weight.objects.filter(created_by=self.created_by)[0].weight

    def last_measure(self):
        instance = Weight.objects.filter(created_by=self.created_by)[0]
        return instance.measurement_date

    def max_weight(self):
        values = [n.weight for n in Weight.objects.filter(created_by=self.created_by)]
        if len(values) == 0:
            return None
        else:
            return max(values)

    def max_weight_one_year(self):
        values = [n.weight for n in Weight.objects.filter(created_by=self.created_by,
                                                            measurement_date__gt=datetime.date(timezone.now().year - 1,
                                                                                               timezone.now().month,
                                                                                               timezone.now().day)
                                                            )]
        if len(values) == 0:
            return None
        else:
            return max(values)

    def min_weight(self):
        values = [n.weight for n in Weight.objects.filter(created_by=self.created_by)]
        if len(values) == 0:
            return None
        else:
            return min(values)

    def min_weight_one_year(self):
        values = [n.weight for n in Weight.objects.filter(created_by=self.created_by,
                                                            measurement_date__gt=datetime.date(timezone.now().year - 1,
                                                                                               timezone.now().month,
                                                                                               timezone.now().day)
                                                            )]
        if len(values) == 0:
            return None
        else:
            return min(values)

    def average_weight(self):
        weights = Weight.objects.filter(created_by=self.created_by)
        if weights.count() == 0:
            return None
        else:
            return round(sum([n.weight for n in weights]) / weights.count(), 1)

    def average_weight_one_year(self):
        data = Weight.objects.filter(created_by=self.created_by,
                                     measurement_date__gt=datetime.date(timezone.now().year - 1,
                                                                        timezone.now().month,
                                                                        timezone.now().day))
        if data.count() == 0:
            return None
        else:
            return round(sum([n.weight for n in data]) / data.count(), 1)

    def get_absolute_url(self):
        return reverse("weight-detail", kwargs={"pk": self.id})

    def get_update_url(self):
        return reverse("weight-update", kwargs={"pk": self.id})

    def get_create_url(self):
        return reverse("weight-create")

    def __str__(self):
        return str(self.measurement_date.strftime("%d.%m.%Y")) + ": " + str(self.weight)
