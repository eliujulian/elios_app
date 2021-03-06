from django.shortcuts import get_object_or_404
from django.forms import modelform_factory
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from core.views import CustomDetailView, CustomUpdateView, CustomCreateView, CustomDeleteView, CustomListView, \
    TemplateView
from habit.forms import *


perm = 'core.habit_app'


class HabitProfileView(PermissionRequiredMixin, CustomDetailView):
    model = HabitProfile
    template_name = 'habit/habitprofile.html'
    http_method_names = ['get']
    permission_required = perm

    def get_object(self, queryset=None):
        instance = get_object_or_404(HabitProfile, profile_for=self.request.user)
        return instance


class HabitProfileUpdateView(PermissionRequiredMixin, CustomUpdateView):
    model = HabitProfile
    permission_required = perm
    template_name = "habit/hapitprofile_update.html"

    def get_object(self, queryset=None):
        instance = get_object_or_404(HabitProfile, profile_for=self.request.user)
        return instance

    def get_form_class(self):
        if self.request.GET.get('field', False):
            field = self.request.GET.get('field', False)
            return modelform_factory(HabitProfile,
                                     fields=[field, ],
                                     labels={field: self.model.LABELS[field]},
                                     widgets={field: forms.Textarea(attrs={"cols": 80, "rows": 20})})
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


class SphereView(PermissionRequiredMixin, TemplateView):
    permission_required = perm
    template_name = "habit/sphere.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_id = self.request.user.id
        sphere = self.kwargs['sphere']
        if sphere > 8 or sphere < 1:
            raise Http404("Sphere must be between 1 - 8")
        habitprofile = HabitProfile.objects.get(profile_for_id=user_id)
        visions = habitprofile.get_visions()[sphere-1]
        context['sphere_id'] = visions[0]
        context['sphere'] = visions[1]
        context['vision'] = visions[2]
        context['goals'] = Goal.objects.filter(created_by_id=user_id, sphere=sphere)
        context['habits'] = Habit.objects.filter(created_by_id=user_id, sphere=sphere)
        return context


class GoalCreateView(PermissionRequiredMixin, CustomCreateView):
    model = Goal
    permission_required = perm
    form_class = GoalForm


class GoalDetailView(PermissionRequiredMixin, CustomDetailView):
    model = Goal
    permission_required = perm
    slug_field = 'id_slug'
    http_method_names = ['get']
    template_name = 'habit/goal_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Goal, created_by=self.request.user, id_slug=self.kwargs['slug'])


class GoalUpdateView(PermissionRequiredMixin, CustomUpdateView):
    model = Goal
    permission_required = perm
    form_class = GoalForm
    slug_field = 'id_slug'

    def get_object(self, queryset=None):
        return get_object_or_404(Goal, created_by=self.request.user, id_slug=self.kwargs['slug'])


class GoalDeleteView(PermissionRequiredMixin, CustomDeleteView):
    model = Goal
    permission_required = perm
    slug_field = 'id_slug'

    def get_object(self, queryset=None):
        return get_object_or_404(Goal, created_by=self.request.user, id_slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse("goals")


class GoalListView(PermissionRequiredMixin, CustomListView):
    model = Goal
    permission_required = perm
    http_method_names = ['get']
    template_name = "habit/goal_list.html"

    def get_queryset(self):
        return Goal.objects.filter(created_by=self.request.user)


class HabitListView(PermissionRequiredMixin, CustomListView):
    model = Habit
    permission_required = perm
    http_method_names = ['get']
    template_name = "habit/habit_list.html"

    def get_queryset(self):
        return Habit.objects.filter(created_by=self.request.user)


class HabitDetailView(PermissionRequiredMixin, CustomDetailView):
    model = Habit
    permission_required = perm
    http_method_names = ['get']
    template_name = "habit/habit_detail.html"

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, created_by=self.request.user, id_slug=self.kwargs['slug'])


class HabitEventView(PermissionRequiredMixin, CustomDetailView):
    model = Habit
    permission_required = perm
    http_method_names = ['post']

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, created_by=self.request.user, id_slug=self.kwargs['slug'])


class HabitUpdateView(PermissionRequiredMixin, CustomUpdateView):
    model = Habit
    permission_required = perm
    form_class = HabitForm

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, created_by=self.request.user, id_slug=self.kwargs['slug'])

    def get_form_class(self):
        form = self.form_class
        form.base_fields['goal'].limit_choices_to = {'created_by': self.request.user, 'sphere': self.object.sphere}
        return form


class HabitCreateView(PermissionRequiredMixin, CustomCreateView):
    model = Habit
    permission_required = perm
    form_class = HabitForm

    def get_form_class(self):
        form = self.form_class
        form.base_fields['goal'].limit_choices_to = {'created_by': self.request.user}
        return form


class HabitDeleteView(PermissionRequiredMixin, CustomDeleteView):
    model = Habit
    permission_required = perm
    slug_field = 'id_slug'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, created_by=self.request.user, id_slug=self.kwargs['slug'])
