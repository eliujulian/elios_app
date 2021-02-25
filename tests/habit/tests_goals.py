from django.utils import timezone
from django.test import TestCase
from django.template.response import TemplateResponse
from tests.texts_mixins import *
from habit.views import *


class GoalTests(CreateUserMixin, TestCase):
    def setUp(self) -> None:
        super(GoalTests, self).setUp()
        data = {
            'created_by': self.user,
            'timestamp_created': timezone.now(),
            'timestamp_changed': timezone.now(),
            'sphere': 1,
            'id_slug': Goal.get_id_slug(10),
            'title': "Mein Ziel",
            'description': "Lorem ipsum"
        }
        self.goal = Goal.objects.create(**data)


class GoalListViewTests(GoalTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("goals"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_get(self):
        response = self.client.get(reverse("goals"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['object_list']), 1)

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username="bdam", password="123456")
        response = self.client.get(reverse("goals"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['object_list']), 0)

    def test_post(self):
        response = self.client.post(reverse("goals"))
        self.assertEqual(response.status_code, 405)


class GoalDetailTest(GoalTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("goal-detail", args=[self.goal.id_slug, ]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_get(self):
        response = self.client.get(reverse("goal-detail", args=[self.goal.id_slug, ]))
        self.assertEqual(response.status_code, 200)

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username="bdam", password="123456")
        response = self.client.get(reverse("goal-detail", args=[self.goal.id_slug, ]))
        self.assertEqual(response.status_code, 401)

    def test_post(self):
        response = self.client.post(reverse("goals"))
        self.assertEqual(response.status_code, 405)
