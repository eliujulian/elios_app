import datetime
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


class WeightListTest(WeightClassTests):
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


class WeightDetailViewTest(WeightClassTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("weight-detail", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn("login", response.url)

    def test_response_detail_view_get(self):
        response = self.client.get(reverse("weight-detail", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_response_detail_view_post(self):
        response = self.client.post(reverse("weight-detail", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 405)

    def test_response_user2_detail_view_get_and_post(self):
        self.client.logout()
        self.client.login(username="bdam", password="123456")
        response = self.client.get(reverse("weight-detail", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 404)
        response = self.client.post(reverse("weight-detail", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 405)


class WeightUpdateViewTest(WeightClassTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("weight-update", args=[1, ]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_response_user_update_view(self):
        response = self.client.post(reverse("weight-update", kwargs={'pk': 1}), data={})
        self.assertEqual(response.status_code, 200)

    def test_response_wrong_user(self):
        self.client.logout()
        self.client.login(username="bdam", password="123456")
        response = self.client.get(reverse("weight-update", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 404)
        response = self.client.post(reverse("weight-update", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 404)


class WeightDeleteViewTest(WeightClassTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("weight-delete", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn('login', response.url)
        response = self.client.post(reverse("weight-delete", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn('login', response.url)

    def test_logged_in(self):
        response = self.client.get(reverse("weight-delete", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)
        response = self.client.post(reverse("weight-delete", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertIn("message", response.url)

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username="bdam", password="123456")
        response = self.client.get(reverse("weight-delete", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 404)
        response = self.client.post(reverse("weight-delete", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 404)


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
