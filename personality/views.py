from django.shortcuts import reverse, get_object_or_404
from django.utils import timezone
from django.contrib.auth.mixins import PermissionRequiredMixin
from core.views import CustomDetailView, CustomUpdateView, CustomCreateView, CustomDeleteView
from personality.forms import *


perm = 'core.personality_app'


class PersonalityView(PermissionRequiredMixin, CustomDetailView):
    model = PersonalityProfile
    template_name = "personality/personality.html"
    permission_required = perm

    def get_object(self, queryset=None):
        return PersonalityProfile.objects.get(created_by=self.request.user)


class PersonalityUpdateView(PermissionRequiredMixin, CustomUpdateView):
    model = PersonalityProfile
    form_class = PersonalityUpdateForm
    permission_required = perm

    def get_object(self, queryset=None):
        return PersonalityProfile.objects.get(profile_about=self.request.user)


class PersonalityNoteCreateView(PermissionRequiredMixin, CustomCreateView):
    model = PersonalityNote
    form_class = NoteForm
    permission_required = perm

    def form_valid(self, form):
        form.instance.note_about = self.request.user.personalityprofile
        form.instance.id_slug = self.model.get_id_slug(10)
        return super().form_valid(form)


class PersonalityNoteUpdateView(PermissionRequiredMixin, CustomUpdateView):
    model = PersonalityNote
    form_class = NoteForm
    slug_field = "id_slug"
    permission_required = perm

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, created_by=self.request.user, id_slug=self.kwargs['slug'])


class PersonalityNoteDeleteView(PermissionRequiredMixin, CustomDeleteView):
    model = PersonalityNote
    slug_field = "id_slug"
    permission_required = perm

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, created_by=self.request.user, id_slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse("personality")
