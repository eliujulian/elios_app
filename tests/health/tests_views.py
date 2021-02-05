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
