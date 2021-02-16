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
            'summary': 'Infinite Yest'
        }
        Book.objects.create(**data)


class BookListTest(BookTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse())
