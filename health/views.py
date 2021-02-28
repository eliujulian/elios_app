from django.shortcuts import reverse, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from core.views import CustomListView, CustomDetailView, CustomCreateView, CustomUpdateView, CustomDeleteView
from health.models import Weight
from health.forms import WeightForm


class WeightCreateView(PermissionRequiredMixin, CustomCreateView):
    model = Weight
    form_class = WeightForm
    permission_required = 'core.health_app'


class WeightListView(PermissionRequiredMixin, CustomListView):
    model = Weight
    permission_required = 'core.health_app'

    def get_queryset(self):
        return Weight.objects.filter(created_by=self.request.user)


class WeightDetailView(PermissionRequiredMixin, CustomDetailView):
    model = Weight
    permission_required = 'core.health_app'
    http_method_names = ['get']

    def get_object(self, queryset=None):
        return get_object_or_404(Weight, created_by=self.request.user, id=self.kwargs['pk'])


class WeightUpdateView(PermissionRequiredMixin, CustomUpdateView):
    model = Weight
    form_class = WeightForm
    permission_required = 'core.health_app'

    def get_object(self, queryset=None):
        return get_object_or_404(Weight, created_by=self.request.user, id=self.kwargs['pk'])


class WeightDeleteView(PermissionRequiredMixin, CustomDeleteView):
    model = Weight
    permission_required = 'core.health_app'

    def get_object(self, queryset=None):
        return get_object_or_404(Weight, created_by=self.request.user, id=self.kwargs['pk'])

    def get_success_url(self):
        instance = self.object
        message = f"{instance} was deleted."
        return reverse("message-success-public") + f"?message={message}"
