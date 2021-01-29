from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.shortcuts import reverse
from django.core.mail import send_mail
from elios_app import settings


class User(AbstractUser):
    class Meta:
        ordering = ['id']

    email_confirm_secret = models.CharField(max_length=24, default="")
    email_confirmed = models.BooleanField(default=False)
    timestamp_confirmation_code_send = models.DateTimeField(null=True, blank=True)
    date_deleted = models.DateField(null=True, blank=True)

    def send_email_to_user(self, subject, message):
        subject = subject
        message = message
        email = self.email
        send_mail(
            subject,
            message,
            'elevate@eliu.de',
            [email],
            fail_silently=False,
        )
        return None

    def get_confirm_url(self):
        confirm_url = settings.BASE_URL
        confirm_url += reverse("account-confirm")
        confirm_url += f"?username={self.username}&confirmation_code={self.email_confirm_secret}"
        return confirm_url

    def get_absolute_url(self):
        return reverse("account-detail", kwargs={"slug": self.username})

    def get_delete_url(self):
        return reverse("account-delete", kwargs={"slug": self.username})

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
