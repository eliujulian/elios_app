from django.test import TestCase, Client
from django.template.response import TemplateResponse
from django.shortcuts import reverse
from core.models import User


class CreateUserMixin:
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("adam", "adam@adam.de", "123456")
        self.client.login(username="adam", password="123456")


class LandingpageViewTest(CreateUserMixin, TestCase):
    def test_get_response_status_logged_in(self):
        response = self.client.get(reverse("landingpage"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)
