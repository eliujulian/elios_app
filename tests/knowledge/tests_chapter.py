from django.template.response import TemplateResponse
from knowledge.views import *
from tests.knowledge.tests_book import BookTests


class ChapterTests(BookTests):
    def setUp(self):
        super().setUp()
        self.client.post(
            reverse('chapter-create', args=[self.book.id_slug]),
            data={'title': 'First', 'Summary': 'A Summary'}
        )
        self.client.post(
            reverse('chapter-create', args=[self.book.id_slug]),
            data={'title': 'Second', 'Summary': 'A Summary'}
        )
        self.client.post(
            reverse('chapter-create', args=[self.book.id_slug]),
            data={'title': 'Third', 'Summary': 'A Summary'}
        )
        self.client.post(
            reverse('chapter-create', args=[self.book.id_slug]),
            data={'title': 'Fourth', 'Summary': 'A Summary'}
        )


class BookTest(ChapterTests):
    def test_number_of_chapters(self):
        self.assertEqual(self.book.chapter_set.all().count(), 4)


class ChapterModelTest(ChapterTests):
    def test_chapter_model(self):
        chapter1 = Chapter.objects.get(id=1)
        chapter2 = Chapter.objects.get(id=2)
        self.assertEqual(chapter1.order_num_plus_one(), 1)
        self.assertEqual(chapter1.order_num_minus_one(), -1)
        self.assertFalse(chapter1.previous_chapter())
        self.assertTrue(chapter2.previous_chapter())
        self.assertTrue(chapter2.next_chapter())
        self.assertIsInstance(chapter1.next_chapter(), Chapter)
        self.assertIsInstance(chapter2.next_chapter(), Chapter)


class ChapterCreateTests(ChapterTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('chapter-create', args=[self.book.id_slug, ]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username="bdam", password="123456")
        response = self.client.get(reverse('chapter-create', args=[self.book.id_slug, ]))
        self.assertEqual(response.status_code, 401)
        response = self.client.post(reverse('chapter-create', args=[self.book.id_slug, ]))
        self.assertEqual(response.status_code, 401)

    def test_get(self):
        response = self.client.get(reverse('chapter-create', args=[self.book.id_slug, ]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_post(self):
        response = self.client.post(reverse('chapter-create', args=[self.book.id_slug, ]),
                                    data={'title': "Fith"})
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(self.book.chapter_set.all().count(), 5)


class ChapterDetailTest(ChapterTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('chapter-detail', args=[self.book.id_slug, 0]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username="bdam", password="123456")
        response = self.client.get(reverse('chapter-detail', args=[self.book.id_slug, 0]))
        self.assertEqual(response.status_code, 401)

    def test_get(self):
        response = self.client.get(reverse('chapter-detail', args=[self.book.id_slug, 0]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(response.context_data['object'].title, "First")

    def test_post(self):
        response = self.client.post(reverse('chapter-detail', args=[self.book.id_slug, 0]))
        self.assertEqual(response.status_code, 405)


class ChapterUpdateTest(ChapterTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('chapter-update', args=[self.book.id_slug, 0]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username="bdam", password="123456")
        response = self.client.get(reverse('chapter-update', args=[self.book.id_slug, 0]))
        self.assertEqual(response.status_code, 401)

    def test_get(self):
        response = self.client.get(reverse('chapter-update', args=[self.book.id_slug, 0]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)
        self.assertEqual(response.context_data['object'].title, "First")

    def test_post(self):
        response = self.client.post(reverse('chapter-update', args=[self.book.id_slug, 0]),
                                    data={'title': 'Erstes'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.book.chapter_set.get(order_num=0).title, 'Erstes')


class ChapterDeleteTest(ChapterTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('chapter-delete', args=[self.book.id_slug, 0]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username="bdam", password="123456")
        response = self.client.get(reverse('chapter-delete', args=[self.book.id_slug, 0]))
        self.assertEqual(response.status_code, 401)

    def test_get(self):
        response = self.client.get(reverse('chapter-delete', args=[self.book.id_slug, 0]))
        self.assertEqual(response.status_code, 200)

    def test_post_delete_0(self):
        response = self.client.post(reverse('chapter-delete', args=[self.book.id_slug, 0]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.book.chapter_set.all().count(), 3)
        self.assertEqual(self.book.chapter_set.get(order_num=0).title, "Second")

    def test_post_delete_1(self):
        response = self.client.post(reverse('chapter-delete', args=[self.book.id_slug, 1]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.book.chapter_set.all().count(), 3)
        self.assertEqual(self.book.chapter_set.get(order_num=1).title, "Third")


class ChapterRandomTest(ChapterTests):
    def test_random(self):
        self.assertTrue(self.book.chapter_set.all().count() > 3)
        response = self.client.get(reverse("chapter-random"))
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn('chapter', response.url)
        self.assertNotIn('message', response.url)


class ChapterChangeOrderTest(ChapterTests):
    def test_up(self):
        response = self.client.get(reverse("chapter-up", args=[self.book.id_slug, 0, ]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.book.chapter_set.all().first().title, "Second")
        self.assertEqual(self.book.chapter_set.all().last().title, "Fourth")
        response = self.client.get(reverse("chapter-up", args=[self.book.id_slug, 3, ]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.book.chapter_set.all().last().title, "Fourth")

    def test_down(self):
        response = self.client.get(reverse("chapter-down", args=[self.book.id_slug, 1, ]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.book.chapter_set.all().first().title, "Second")

    def test_down_first(self):
        self.assertEqual(self.book.chapter_set.all().first().title, "First")
        response = self.client.get(reverse("chapter-down", args=[self.book.id_slug, 0, ]))
        self.assertEqual(self.book.chapter_set.all().first().title, "First")
