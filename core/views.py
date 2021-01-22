from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.http import HttpResponseForbidden, HttpResponse
from .models import *
from .forms import *


class CustomCreateView(CreateView):
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.timestamp_created = timezone.now()
        form.instance.timestamp_changed = timezone.now()
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        for field in self.form_class().fields:
            if self.request.GET.get(field, False):
                initial[field] = self.request.GET.get(field)
        return initial


class CustomDetailView(DetailView):
    pass


class CustomUpdateView(UpdateView):
    pass


class CustomListView(ListView):
    pass


class CustomDeleteView(DeleteView):
    pass


class UserDetailView(CustomDetailView):
    model = User
    template_name = "generic/generic_detail.html"
    slug_field = "username"


class AccountDetailView(CustomDetailView):
    model = User
    template_name = "generic/generic_detail.html"
    slug_field = "username"

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            return HttpResponse("Unauthorized", status=401)
        else:
            return super().get(request)


class AccountUpdateView(CustomUpdateView):
    model = User
    template_name = "generic/generic_update.html"
    slug_field = "username"
    form_class = AccountUpdateForm


class AccountDeleteView(CustomDeleteView):
    model = User
    slug_field = "username"
