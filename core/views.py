import random
import string
import datetime
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import *
from elios_app import settings


class CustomCreateView(CreateView):
    template_name = "generic/generic_create.html"

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
    template_name = "generic/generic_detail.html"


class CustomUpdateView(UpdateView):
    template_name = "generic/generic_update.html"


class CustomListView(ListView):
    template_name = "generic/generic_list.html"


class CustomDeleteView(DeleteView):
    template_name = "generic/generic_confirm_delete.html"


class OnlyCreatorAccessMixin:
    def get(self, request, *args, **kwargs):
        instance = self.get_object() # noqa
        if request.user != instance.created_by:
            return HttpResponse("Unauthorized", status=401)
        return super().get(request, *args, **kwargs) # noqa

    def post(self, request, *args, **kwargs):
        instance = self.get_object() # noqa
        if request.user != instance.created_by:
            return HttpResponse("Unauthorized", status=401)
        return super().post(request, *args, **kwargs) # noqa


class UserDetailView(PermissionRequiredMixin, CustomDetailView):
    model = User
    template_name = "user/user_detail.html"
    slug_field = "username"
    permission_required = 'core.landingpage_right'

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

        # add for all new users to group "standard-users
        Group.objects.get(name="StandardUsers").user_set.add(self.object)

        confirm_url = self.object.get_confirm_url()

        if settings.ALLOW_SENDING_CONFIRMATION_EMAILS:
            self.object.send_email_to_user(
                subject="Please confirm your account",
                message=f"Hello {self.object}, \n please copy&paste the following link "
                        f"to your browser to confirm your account. \n {confirm_url}",
            )
            self.object.timestamp_confirmation_code_send = timezone.now()
            self.object.save()
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
    http_method_names = ["get"]

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


class AccountDetailView(PermissionRequiredMixin, CustomDetailView):
    model = User
    slug_field = "username"
    permission_required = 'core.landingpage_right'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            return HttpResponse("Unauthorized", status=401)
        else:
            return super().get(request, *args, **kwargs)


class AccountUpdateView(PermissionRequiredMixin, CustomUpdateView):
    model = User
    slug_field = "username"
    form_class = AccountUpdateForm
    permission_required = 'core.landingpage_right'

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


class AccountDeleteView(PermissionRequiredMixin, CustomDeleteView):
    model = User
    slug_field = "username"
    permission_required = 'core.landingpage_right'

    def get_success_url(self):
        instance = self.get_object()
        message = f"{instance} was deleted."
        return reverse("message-success-public") + f"?message={message}"

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

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        success_url = self.get_success_url()
        instance.is_active = False
        instance.date_deleted = datetime.datetime.today()
        instance.save()
        logout(request)
        return HttpResponseRedirect(success_url)
