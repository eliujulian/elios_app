from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client
from core.models import User, PermissionRegister


class CreateStandardGroupsMixin:
    def setUp(self):
        Group.objects.create(**{'name': "PersonalityApp"})
        Group.objects.create(**{'name': "HabitApp"})
        Group.objects.create(**{'name': "HealthApp"})
        group_standard = Group.objects.create(**{'name': "StandardUsers"})

        group_standard.permissions.add(Permission.objects.get(
            content_type=ContentType.objects.get_for_model(PermissionRegister),
            codename="landingpage_right"))
        group_standard.permissions.add(Permission.objects.get(
            content_type=ContentType.objects.get_for_model(PermissionRegister),
            codename="knowledge_app"))
        group_standard.permissions.add(Permission.objects.get(
            content_type=ContentType.objects.get_for_model(PermissionRegister),
            codename="habit_app"))
        group_standard.permissions.add(Permission.objects.get(
            content_type=ContentType.objects.get_for_model(PermissionRegister),
            codename="health_app"))


class CreateUserMixin(CreateStandardGroupsMixin):
    def setUp(self):
        super().setUp() # noqa
        self.client = Client()

        password = "123456"
        data = {"username": "adam", "first_name": "Adam", "last_name": "Test", "password": password}
        data_2 = {"username": "bdam", "first_name": "Bert", "last_name": "Test", "password": password}

        self.client.post(reverse("account-register"), data=data)
        self.client.post(reverse("account-register"), data=data_2)
        self.user = User.objects.get(username="adam")
        self.user.is_active = True
        self.user.save()
        self.user2 = User.objects.get(username="bdam")
        self.user2.is_active = True
        self.user2.save()
        self.client.login(username="adam", password=password)

