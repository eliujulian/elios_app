from django.test import TestCase
from core.models import *


class UserModelTest(TestCase):
    def test_get_confirm_url(self):
        data = {"username": "adam", "password": "password", "email": "example@eliu.de" }
        self.client.post(reverse("account-register"), data=data)
        user = User.objects.get(username="adam")
        self.assertIn("127.0.0.1", user.get_confirm_url())
        self.assertIn("adam", user.get_confirm_url())
