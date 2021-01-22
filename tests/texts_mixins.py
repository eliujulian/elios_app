from django.test import Client
from core.models import User


class CreateUserMixin:
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("adam", "adam@adam.de", "123456")
        self.user2 = User.objects.create_user("bdam", "adam@adam.de", "123456")
        self.client.login(username="adam", password="123456")
