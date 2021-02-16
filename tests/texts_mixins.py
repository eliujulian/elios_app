from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.test import Client
from core.models import User, PermissionRegister


class CreateStandardGroupsMixin:
    def setUp(self):
        group_standard = Group.objects.create(**{'name': "StandardUsers"})
        group_standard.permissions.add(Permission.objects.get(
            content_type=ContentType.objects.get_for_model(PermissionRegister),
            codename="landingpage_right"))
        group_standard.permissions.add(Permission.objects.get(
            content_type=ContentType.objects.get_for_model(PermissionRegister),
            codename="knowledge_app"))
        group_health = Group.objects.create(**{'name': "HealthApp"})
        group_health.permissions.add(Permission.objects.get(
            content_type=ContentType.objects.get_for_model(PermissionRegister),
            codename="health_app"))


class CreateUserMixin(CreateStandardGroupsMixin):
    def setUp(self):
        super().setUp() # noqa
        self.client = Client()
        self.user = User.objects.create_user("adam", "adam@adam.de", "123456")
        self.user2 = User.objects.create_user("bdam", "adam@adam.de", "123456")
        Group.objects.get(name="StandardUsers").user_set.add(self.user)
        Group.objects.get(name="StandardUsers").user_set.add(self.user2)
        Group.objects.get(name="HealthApp").user_set.add(self.user)
        Group.objects.get(name="HealthApp").user_set.add(self.user2)
        self.client.login(username="adam", password="123456")
