from django.utils import timezone
from django.test import TestCase
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

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username="bdam", password="123456")
        response = self.client.get(reverse("goals"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['object_list']), 0)

    def test_get(self):
        response = self.client.get(reverse("goals"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['object_list']), 1)

    def test_post(self):
        response = self.client.post(reverse("goals"))
        self.assertEqual(response.status_code, 405)


class GoalDetailTest(GoalTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("goal-detail", args=[self.goal.id_slug, ]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username="bdam", password="123456")
        response = self.client.get(reverse("goal-detail", args=[self.goal.id_slug, ]))
        self.assertEqual(response.status_code, 401)

    def test_get(self):
        response = self.client.get(reverse("goal-detail", args=[self.goal.id_slug, ]))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(reverse("goals"))
        self.assertEqual(response.status_code, 405)


class GoalUpdateTest(GoalTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("goal-update", args=[self.goal.id_slug, ]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username="bdam", password="123456")
        response = self.client.get(reverse("goal-update", args=[self.goal.id_slug, ]))
        self.assertEqual(response.status_code, 401)
        response = self.client.post(reverse("goal-update", args=[self.goal.id_slug, ]))
        self.assertEqual(response.status_code, 401)

    def test_get(self):
        response = self.client.get(reverse("goal-update", args=[self.goal.id_slug, ]))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(reverse("goal-update", args=[self.goal.id_slug, ]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("goal-update", args=[self.goal.id_slug, ]), data={'title': 'Neuer Titel',
                                                                                              'sphere': 1})
        self.assertEqual(response.status_code, 302)


class GoalCreateTest(GoalTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("goal-create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_get(self):
        response = self.client.get(reverse("goal-create"))
        self.assertEqual(response.status_code, 200)

    def test_post_invalid(self):
        response = self.client.post(reverse("goal-create"))
        self.assertEqual(response.status_code, 200)

    def test_post_valid(self):
        data = {'title': 'Titel', 'sphere': 1}
        response = self.client.post(reverse("goal-create"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertIn("goal", response.url)


class GoalDeleteTest(GoalTests):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("goal-delete", args=[self.goal.id_slug, ]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_wrong_user(self):
        self.client.logout()
        self.client.login(username="bdam", password="123456")
        response = self.client.get(reverse("goal-delete", args=[self.goal.id_slug, ]))
        self.assertEqual(response.status_code, 401)
        response = self.client.post(reverse("goal-delete", args=[self.goal.id_slug, ]))
        self.assertEqual(response.status_code, 401)

    def test_get(self):
        response = self.client.get(reverse("goal-delete", args=[self.goal.id_slug, ]))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(reverse("goal-delete", args=[self.goal.id_slug, ]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Goal.objects.filter(created_by=self.user).count(), 0)
