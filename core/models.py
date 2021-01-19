from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    class Meta:
        ordering = ['id']

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username


class AbstractBaseModel(models.Model):
    class Meta:
        abstract = True

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", blank=True)
    timestamp_created = models.DateTimeField()
    timestamp_changed = models.DateTimeField()

    def clean(self):
        if not self.timestamp_created:
            self.timestamp_created = timezone.now()
        self.timestamp_changed = timezone.now()

    def get_absolute_url(self):
        raise Exception("Improperly configured, please configure get_absolute_url function.")

    def get_update_url(self):
        return self.get_absolute_url() + "update/"

    def get_overview_url(self):
        raise Exception("Improperly configured, please configure get_overview_url function.")

    def get_create_url(self):
        raise Exception("Improperly configured, please configure get_create_url function.")
