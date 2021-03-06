from django.utils import timezone
from django.test import TestCase
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from tests.texts_mixins import *
from health.views import *


class WeightClassTests(CreateUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        data = {
            'created_by': self.user,
            'timestamp_created': timezone.now(),
            'timestamp_changed': timezone.now(),
            'weight': 80.8,
            'measurement_date': datetime.date(2020, 1, 1)
        }
        Weight.objects.create(**data)
        data = {
            'created_by': self.user2,
            'timestamp_created': timezone.now(),
            'timestamp_changed': timezone.now(),
            'weight': 80.8,
            'measurement_date': datetime.date(2020, 1, 1)
        }
        Weight.objects.create(**data)


class WeightTest(WeightClassTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("weight"))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn("login", response.url)

    def test_response(self):
        response = self.client.get(reverse("weight"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_post(self):
        response = self.client.post(reverse("weight"))
        self.assertEqual(response.status_code, 405)

    def test_with_data(self):
        response = self.client.get(reverse("weight"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)
        self.client.logout()
        self.client.login(username="bdam", password="123456")
        response = self.client.get(reverse("weight"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)


class WeightTestNoData(CreateUserMixin, TestCase):
    def test_get(self):
        response = self.client.get(reverse("weight"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)
        self.assertFalse(response.context_data['object'])


class WeightCreateTest(WeightClassTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("weight-create"))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn('login', response.url)
        response = self.client.post(reverse("weight-create"))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn('login', response.url)

    def test_logged_in_get(self):
        response = self.client.get(reverse("weight-create"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_logged_in_post_not_valid_data(self):
        response = self.client.post(reverse("weight-create"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_logged_in_post_valid_data(self):
        data = {"weight": 80, "measurement_date": datetime.date(2020, 1, 1)}
        response = self.client.post(reverse("weight-create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Weight.objects.filter(created_by_id=1).count(), 2)
        self.assertEqual(response.url, "/health/weight/")
