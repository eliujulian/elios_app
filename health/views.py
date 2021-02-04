from core.views import CustomListView, CustomDetailView
from health.models import Weight


class WeightListView(CustomListView):
    model = Weight
    template_name = "generic/generic_list.html"

    def get_queryset(self):
        return Weight.objects.filter(created_by=self.request.user)


class WeightDetailView(CustomDetailView):
    model = Weight
    template_name = "generic/generic_detail.html"
