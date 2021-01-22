from django.forms import ModelForm
from core.models import *


class AccountUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
        ]
