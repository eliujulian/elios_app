from django.http import HttpResponse
from core.views import CustomListView, CustomDetailView, CustomCreateView, CustomUpdateView
from health.models import Weight
from health.forms import WeightForm


class WeightCreateView(CustomCreateView):
    model = Weight
    form_class = WeightForm


class WeightListView(CustomListView):
    model = Weight

    def get_queryset(self):
        return Weight.objects.filter(created_by=self.request.user)


class WeightDetailView(CustomDetailView):
    model = Weight

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.created_by:
            return HttpResponse("Unauthorized", status=401)
        return super().get(request, *args, **kwargs)


class WeightUpdateView(CustomUpdateView):
    model = Weight
    form_class = WeightForm
