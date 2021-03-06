import datetime
from django.shortcuts import reverse, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from core.views import CustomListView, CustomDetailView, CustomCreateView, CustomUpdateView, CustomDeleteView
from health.models import Weight
from health.forms import WeightForm


class WeightCreateView(PermissionRequiredMixin, CustomCreateView):
    model = Weight
    form_class = WeightForm
    permission_required = 'core.health_app'

    def get_initial(self):
        initials = super(WeightCreateView, self).get_initial()
        initials['measurement_date'] = datetime.date.today()
        return initials


class WeightView(PermissionRequiredMixin, CustomDetailView):
    model = Weight
    permission_required = 'core.health_app'
    template_name = "health/health.html"
    http_method_names = ['get']

    def get_object(self, queryset=None):
        instance = Weight.objects.filter(created_by=self.request.user).first()
        return instance
