from django.shortcuts import reverse
from django.utils import timezone
from django.contrib.auth.mixins import PermissionRequiredMixin
from core.views import CustomDetailView, CustomUpdateView, CustomCreateView, CustomDeleteView, OnlyCreatorAccessMixin
from personality.forms import *


class PersonalityView(PermissionRequiredMixin, CustomDetailView):
    model = PersonalityProfile
    template_name = "personality/personality.html"
    permission_required = 'core.personality_app'

    def get_object(self, queryset=None):
        if PersonalityProfile.objects.filter(profile_about=self.request.user).count() == 0:
            PersonalityProfile.objects.create(
                **{'created_by': self.request.user,
                   'profile_about': self.request.user,
                   'timestamp_created': timezone.now(),
                   'timestamp_changed': timezone.now()}
            )
        return PersonalityProfile.objects.get(profile_about=self.request.user)


class PersonalityUpdateView(PermissionRequiredMixin, CustomUpdateView):
    model = PersonalityProfile
    form_class = PersonalityUpdateForm
    permission_required = 'core.personality_app'

    def get_object(self, queryset=None):
        return PersonalityProfile.objects.get(profile_about=self.request.user)


class PersonalityNoteCreateView(PermissionRequiredMixin, CustomCreateView):
    model = PersonalityNote
    form_class = NoteForm
    permission_required = 'core.personality_app'

    def form_valid(self, form):
        form.instance.note_about = self.request.user.personalityprofile
        form.instance.id_slug = self.model.get_id_slug(10)
        return super().form_valid(form)


class PersonalityNoteUpdateView(PermissionRequiredMixin, OnlyCreatorAccessMixin, CustomUpdateView):
    model = PersonalityNote
    form_class = NoteForm
    slug_field = "id_slug"
    permission_required = 'core.personality_app'


class PersonalityNoteDeleteView(PermissionRequiredMixin, OnlyCreatorAccessMixin, CustomDeleteView):
    model = PersonalityNote
    slug_field = "id_slug"
    permission_required = 'core.personality_app'

    def get_success_url(self):
        return reverse("personality")
