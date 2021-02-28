from django.test import TestCase
from tests.texts_mixins import *
from habit.views import *


class HabitProfileTests(CreateUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.user.habitprofile.vision_1 = "Arbeit Adam"
        self.user.habitprofile.save()
        self.user2.habitprofile.vision_1 = "Arbeit Bert"
        self.user2.habitprofile.save()

    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("habitprofile"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_get_other_user(self):
        self.client.logout()
        self.client.login(username="bdam", password="123456")
        response = self.client.get(reverse("habitprofile"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['habitprofile'].vision_1, "Arbeit Bert")

    def test_get(self):
        response = self.client.get(reverse("habitprofile"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['habitprofile'].vision_1, "Arbeit Adam")


class HabitProfileUpdateTests(CreateUserMixin, TestCase):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("habitprofile-update"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_get(self):
        response = self.client.get(reverse("habitprofile-update"))
        self.assertEqual(response.status_code, 200)

    def test_post_no_data(self):
        response = self.client.post(reverse("habitprofile-update"))
        self.assertEqual(response.status_code, 302)
