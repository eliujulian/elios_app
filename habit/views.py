from django.utils import timezone
from django.forms import modelform_factory
from django.contrib.auth.mixins import PermissionRequiredMixin
from core.views import CustomDetailView, CustomUpdateView
from habit.forms import *


perm = 'core.habit_app'


class HabitProfileView(PermissionRequiredMixin, CustomDetailView):
    model = HabitProfile
    template_name = 'habit/habitprofile.html'
    http_method_names = ['get']
    permission_required = perm

    def get_object(self, queryset=None):
        if HabitProfile.objects.filter(profile_for=self.request.user).count() == 0:
            HabitProfile.objects.create(
                **{'created_by': self.request.user,
                   'timestamp_created': timezone.now(),
                   'timestamp_changed': timezone.now(),
                   'profile_for': self.request.user
                   }
            )
        return HabitProfile.objects.get(profile_for=self.request.user)


class HabitProfileUpdateView(PermissionRequiredMixin, CustomUpdateView):
    model = HabitProfile
    permission_required = perm
    template_name = "habit/hapitprofile_update.html"

    def get_form_class(self):
        if self.request.GET.get('field', False):
            field = self.request.GET.get('field', False)
            return modelform_factory(HabitProfile, fields=[field, ], labels={field: self.model.LABELS[field]})
        else:
            return HabitProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('field', False):
            field = self.request.GET.get('field', False)
            print(field)
            context['get_parameter'] = f"field={field}"
        print(context)
        return context

    def get_object(self, queryset=None):
        return HabitProfile.objects.get(profile_for=self.request.user)
