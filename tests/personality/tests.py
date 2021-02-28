from django.test import TestCase
from tests.texts_mixins import *
from personality.models import *


class PersonalityDetailViewTest(CreateUserMixin, TestCase):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("personality"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_get(self):
        response = self.client.get(reverse("personality"))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(reverse("personality"))
        self.assertEqual(response.status_code, 405)


class PersonalityUpdateViewTests(CreateUserMixin, TestCase):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("personality-update"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_get(self):
        response = self.client.get(reverse("personality-update"))
        self.assertEqual(response.status_code, 200)

    def test_post_no_data(self):
        response = self.client.post(reverse("personality-update"))
        print(response.context_data)
        self.assertEqual(response.status_code, 200)

    def test_post_with_data(self):
        data = {
            'open_minded_score': 1,
            'conscientiousness_score': 1,
            'extraversion_score': 1,
            'agreeableness_score': 1,
            'neuroticism_score': 1,
        }
        response = self.client.post(reverse("personality-update"), data=data)
        self.assertEqual(response.status_code, 302)
