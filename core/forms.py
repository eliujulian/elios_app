from django.forms import ModelForm
from core.models import *


class AccountRegisterForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        ]


class AccountUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
        ]
