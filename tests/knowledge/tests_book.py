import datetime
from django.shortcuts import reverse
from django.utils import timezone
from django.test import TestCase
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from tests.texts_mixins import *
from knowledge.views import *


class BookTests(CreateUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        data = {
            'created_by': self.user,
            'timestamp_created': timezone.now(),
            'timestamp_changed': timezone.now(),
            'title': 'Unendlicher Spaß',
            'author': 'David Foster Wallace',
            'year': 1995,
            'summary': 'Infinite Yest',
            'id_slug': Book.get_id_slug(10),
        }
        Book.objects.create(**data)


class BookListTest(BookTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_response_get(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_number_of_objects(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object_list'].count(), 1)
        self.client.logout()
        self.client.login(username="bdam", password="123456")
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object_list'].count(), 0)

