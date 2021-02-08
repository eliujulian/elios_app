from django.test import TestCase
from django.contrib.auth.models import Group, Permission, ContentType
from core.models import *
from tests.texts_mixins import CreateStandardGroupsMixin


class UserModelTest(CreateStandardGroupsMixin, TestCase):
    def test_get_confirm_url(self):
        data = {"username": "adam", "password": "password", "email": "example@eliu.de" }
        self.client.post(reverse("account-register"), data=data)
        user = User.objects.get(username="adam")
        self.assertIn("127.0.0.1", user.get_confirm_url())
        self.assertIn("adam", user.get_confirm_url())
        self.assertIn(user.email_confirm_secret, user.get_confirm_url())
