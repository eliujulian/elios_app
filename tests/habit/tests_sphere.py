from django.test import TestCase
from tests.texts_mixins import *
from habit.views import *


class SphereTests(CreateUserMixin, TestCase):
    def setUp(self):
        super().setUp()

    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("sphere", args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_get(self):
        response = self.client.get(reverse("sphere", args=[1]))
        self.assertEqual(response.status_code, 200)
        data = response.context_data
        self.assertEqual(data['sphere'], "Arbeit")

    def test_post(self):
        response = self.client.post(reverse("sphere", args=[1]))
        self.assertEqual(response.status_code, 405)

    def test_wrong_index(self):
        response = self.client.get(reverse("sphere", args=[0]))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse("sphere", args=[9]))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse("sphere", args=[100]))
        self.assertEqual(response.status_code, 404)
