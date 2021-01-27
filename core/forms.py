from django.forms import ModelForm, ValidationError
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

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")

        if len(username) < 4:
            error = ValidationError('username to short')
            self.add_error('username', error)


class AccountUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
        ]
