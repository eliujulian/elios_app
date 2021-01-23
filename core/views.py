import random
import string
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponseNotFound
from .forms import *
from elios_app import settings


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

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_active:
            return HttpResponseNotFound("Not found.")
        else:
            return super().get(request, *args, **kwargs)


class MessageView(TemplateView):
    template_name = "generic/generic_message_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = self.request.GET.get("message")
        return context


class AccountRegisterView(CreateView):
    model = User
    template_name = "generic/generic_create.html"
    form_class = AccountRegisterForm

    def form_valid(self, form):
        super().form_valid(form)
        self.object.email_confirm_secret = ''.join(random.choices(string.ascii_uppercase + string.digits, k=24))
        self.object.is_active = False
        self.object.set_password(raw_password=form.data['password'])
        self.object.save()
        confirm_url = self.object.get_confirm_url()

        if settings.ALLOW_SENDING_CONFIRMATION_EMAILS:
            self.object.send_email_to_user(
                subject="Please confirm your account",
                message=f"Hello {self.object}, \n please copy&paste the following link "
                        f"to your browser to confirm your account. \n {confirm_url}",
            )
        else:
            print("Warning: E-Mail was not send.")

        return super().form_valid(form)

    def get_success_url(self):
        url = reverse("message-success-public")
        if settings.ALLOW_SENDING_CONFIRMATION_EMAILS:
            url += "?message='You created a new account. Check your E-Mail for further details an confirmation.'"
        else:
            url += "?message='You created a new account. Account validation is temporarily suspended."
        return url


class AccountConfirmEMailView(View):
    def get(self, request):
        username = self.request.GET.get("username")
        confirmation_code = self.request.GET.get("confirmation_code")

        if username and confirmation_code:
            user = User.objects.filter(username=username).first()
            if user:
                if user.email_confirm_secret == confirmation_code:
                    user.is_active = True
                    user.email_confirmed = True
                    user.save()
                    url = reverse("message-success-public")
                    url += "?message=E-Mail confirmed. Welcome! You can use the App now!"
                    return redirect(url)

        url = reverse("message-failure-public")
        url += "?message=Confirmation not successful."
        return HttpResponseRedirect(url)

    def post(self, request):
        return HttpResponseNotAllowed(["get"])


class AccountDetailView(CustomDetailView):
    model = User
    template_name = "generic/generic_detail.html"
    slug_field = "username"

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            return HttpResponse("Unauthorized", status=401)
        else:
            return super().get(request, *args, **kwargs)


class AccountUpdateView(CustomUpdateView):
    model = User
    template_name = "generic/generic_update.html"
    slug_field = "username"
    form_class = AccountUpdateForm

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            return HttpResponse("Unauthorized", status=401)
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            return HttpResponse("Unauthorized", status=401)
        else:
            return super().post(request, *args, **kwargs)


class AccountDeleteView(CustomDeleteView):
    model = User
    slug_field = "username"
    template_name = "generic/generic_confirm_delete.html"

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            return HttpResponse("Unauthorized", status=401)
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            return HttpResponse("Unauthorized", status=401)
        else:
            return super().post(request, *args, **kwargs)
