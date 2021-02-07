from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.test import Client
from core.models import User, PermissionRegister


class CreateUserMixin:
    def setUp(self):
        group_standard = Group.objects.create(**{'name': "StandardUsers"})
        group_standard.permissions.add(Permission.objects.get(
            content_type=ContentType.objects.get_for_model(PermissionRegister),
            codename="landingpage_right"))
        group_health = Group.objects.create(**{'name': "HealthApp"})
        group_health.permissions.add(Permission.objects.get(
            content_type=ContentType.objects.get_for_model(PermissionRegister),
            codename="health_app"))
        self.client = Client()
        self.user = User.objects.create_user("adam", "adam@adam.de", "123456")
        self.user2 = User.objects.create_user("bdam", "adam@adam.de", "123456")
        group_standard.user_set.add(self.user)
        group_standard.user_set.add(self.user2)
        group_health.user_set.add(self.user)
        group_health.user_set.add(self.user2)
        self.client.login(username="adam", password="123456")
