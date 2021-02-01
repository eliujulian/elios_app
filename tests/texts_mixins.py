from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.test import Client
from core.models import User, PermissionRegister


class CreateUserMixin:
    def setUp(self):
        perm = Permission.objects.get(content_type=ContentType.objects.get_for_model(PermissionRegister))
        group = Group.objects.create(**{'name': "StandardUsers"})
        group.permissions.add(perm)
        self.client = Client()
        self.user = User.objects.create_user("adam", "adam@adam.de", "123456")
        group.user_set.add(self.user)
        self.user2 = User.objects.create_user("bdam", "adam@adam.de", "123456")
        self.client.login(username="adam", password="123456")
