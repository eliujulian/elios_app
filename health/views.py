from django.http import HttpResponse
from django.shortcuts import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin
from core.views import CustomListView, CustomDetailView, CustomCreateView, CustomUpdateView, CustomDeleteView, \
    OnlyCreatorAccessMixin
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


class WeightDetailView(PermissionRequiredMixin, OnlyCreatorAccessMixin, CustomDetailView):
    model = Weight
    permission_required = 'core.health_app'
    http_method_names = ['get']


class WeightUpdateView(PermissionRequiredMixin, OnlyCreatorAccessMixin, CustomUpdateView):
    model = Weight
    form_class = WeightForm
    permission_required = 'core.health_app'


class WeightDeleteView(PermissionRequiredMixin, OnlyCreatorAccessMixin, CustomDeleteView):
    model = Weight
    permission_required = 'core.health_app'

    def get_success_url(self):
        instance = self.object
        message = f"{instance} was deleted."
        return reverse("message-success-public") + f"?message={message}"
