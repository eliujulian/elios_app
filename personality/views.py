from django.shortcuts import reverse
from django.utils import timezone
from core.views import CustomDetailView, CustomUpdateView, CustomCreateView, CustomDeleteView
from personality.forms import *


class PersonalityView(CustomDetailView):
    model = PersonalityProfile
    template_name = "personality/personality.html"

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


class PersonalityNoteCreateView(CustomCreateView):
    model = PersonalityNote
    form_class = NoteForm

    def form_valid(self, form):
        form.instance.note_about = self.request.user.personalityprofile
        form.instance.id_slug = self.model.get_id_slug(10)
        return super().form_valid(form)


class PersonalityNoteUpdateView(CustomUpdateView):
    model = PersonalityNote
    form_class = NoteForm
    slug_field = "id_slug"


class PersonalityNoteDeleteView(CustomDeleteView):
    model = PersonalityNote
    slug_field = "id_slug"

    def get_success_url(self):
        return reverse("personality")
