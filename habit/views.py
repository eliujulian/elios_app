from django.shortcuts import get_object_or_404
from django.forms import modelform_factory
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from core.views import CustomDetailView, CustomUpdateView, CustomCreateView, CustomDeleteView, CustomListView
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

    def get_queryset(self):
        return Goal.objects.filter(created_by=self.request.user)


class HabitListView(PermissionRequiredMixin, CustomListView):
    model = Habit
    permission_required = perm
    http_method_names = ['get']

    def get_queryset(self):
        return Habit.objects.filter(created_by=self.request.user)


class HabitDetailView(PermissionRequiredMixin, CustomDetailView):
    model = Habit
    permission_required = perm
    http_method_names = ['get']

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, created_by=self.request.user, id_slug=self.kwargs['slug'])


class HabitUpdateView(PermissionRequiredMixin, CustomUpdateView):
    model = Habit
    permission_required = perm

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, created_by=self.request.user, id_slug=self.kwargs['slug'])


class HabitCreateView(PermissionRequiredMixin, CustomCreateView):
    model = Habit
    permission_required = perm
    form_class = HabitForm


class HabitDeleteView(PermissionRequiredMixin, CustomDeleteView):
    model = Habit
    permission_required = perm
    slug_field = 'id_slug'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, created_by=self.request.user, id_slug=self.kwargs['slug'])
