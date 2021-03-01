from django.test import TestCase
from tests.texts_mixins import *
from habit.views import *


class HabitTests(CreateUserMixin):
    def setUp(self):
        super(HabitTests, self).setUp()
        data = {
            'created_by': self.user,
            'timestamp_created': timezone.now(),
            'timestamp_changed': timezone.now(),
            'title': 'Ein Habit',
            'id_slug': Habit.get_id_slug(10),
        }
        self.habit1 = Habit.objects.create(**data)  #nopa


class HabitDetailTest(HabitTests, TestCase):
    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("habit-detail", args=[self.habit1.id_slug, ]))
        self.assertEqual(response.status_code, 302)

    def test_get(self):
        response = self.client.get(reverse("habit-detail", args=[self.habit1.id_slug, ]))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(reverse("habit-detail", args=[self.habit1.id_slug, ]))
        self.assertEqual(response.status_code, 405)
