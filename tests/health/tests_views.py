import datetime
from django.utils import timezone
from django.test import TestCase
from django.template.response import TemplateResponse
from django.shortcuts import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed
from tests.texts_mixins import *
from health.views import *


class WeightListTest(CreateUserMixin, TestCase):
    def test_response(self):
        response = self.client.get(reverse("health-weight"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_get_response_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("health-weight"))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)

    def test_with_data(self):
        data = {
            'created_by': self.user,
            'timestamp_created': timezone.now(),
            'timestamp_changed': timezone.now(),
            'weight': 80.8,
            'measurement_date': datetime.date(2020, 1, 1)
        }
        Weight.objects.create(**data)
        response = self.client.get(reverse("health-weight"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(response.context_data['object_list'].count(), 1)
        self.client.logout()
        self.client.login(username="bdam", password="123456")
        response = self.client.get(reverse("health-weight"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(response.context_data['object_list'].count(), 0)


