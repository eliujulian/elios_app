from django.shortcuts import render
from django.utils import timezone
from core.views import CustomDetailView, CustomUpdateView
from personality.models import *
from personality.forms import *


class PersonalityView(CustomDetailView):
    model = PersonalityProfile

    def get_object(self, queryset=None):
        if PersonalityProfile.objects.filter(profile_about=self.request.user).count() == 0:
            PersonalityProfile.objects.create(
                **{'created_by': self.request.user,
                   'profile_about': self.request.user,
                   'timestamp_created': timezone.now(),
                   'timestamp_changed': timezone.now()}
            )
        return PersonalityProfile.objects.get(profile_about=self.request.user)


class PersonalityUpdateView(CustomUpdateView):
    model = PersonalityProfile
    form_class = PersonalityUpdateForm

    def get_object(self, queryset=None):
        return PersonalityProfile.objects.get(profile_about=self.request.user)
