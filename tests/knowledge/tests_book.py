from django.utils import timezone
from django.test import TestCase
from django.template.response import TemplateResponse
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
        self.book = Book.objects.get(id=1)


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


class BookCreateTest(BookTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('book-create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_get(self):
        response = self.client.get(reverse('book-create'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_post(self):
        response = self.client.post(reverse('book-create'))
        self.assertEqual(response.status_code, 200)


class BookDetailsTest(BookTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("book-detail", args=[self.book.id_slug]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_response_detail_view_get(self):
        response = self.client.get(reverse("book-detail", args=[self.book.id_slug]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_response_detail_view_post(self):
        response = self.client.post(reverse("book-detail", args=[self.book.id_slug]))
        self.assertEqual(response.status_code, 405)

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username="bdam", password="123456")
        response = self.client.get(reverse("book-detail", args=[self.book.id_slug]))
        self.assertEqual(response.status_code, 401)
        response = self.client.post(reverse("book-detail", args=[self.book.id_slug]))
        self.assertEqual(response.status_code, 405)


class BookUpdateTest(BookTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("book-update", args=[self.book.id_slug]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_get(self):
        response = self.client.get(reverse("book-update", args=[self.book.id_slug]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_post(self):
        response = self.client.post(reverse("book-update", args=[self.book.id_slug]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username="bdam", password="123456")
        self.assertEqual(self.client.get(reverse("book-update", args=[self.book.id_slug])).status_code, 401)
        self.assertEqual(self.client.post(reverse("book-update", args=[self.book.id_slug])).status_code, 401)


class BookDeleteTest(BookTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("book-delete", args=[self.book.id_slug]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_get(self):
        self.assertEqual(Book.objects.filter(created_by_id=1).count(), 1)
        response = self.client.get(reverse("book-delete", args=[self.book.id_slug]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(Book.objects.filter(created_by_id=1).count(), 1)

    def test_post(self):
        self.assertEqual(Book.objects.filter(created_by_id=1).count(), 1)
        response = self.client.post(reverse("book-delete", args=[self.book.id_slug]))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(Book.objects.filter(created_by_id=1).count(), 0)

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username="bdam", password="123456")
        self.assertEqual(self.client.get(reverse("book-delete", args=[self.book.id_slug])).status_code, 401)
        self.assertEqual(self.client.post(reverse("book-delete", args=[self.book.id_slug])).status_code, 401)
