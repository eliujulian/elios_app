# Generated by Django 3.1.5 on 2021-02-07 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_permissionregister'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='permissionregister',
            options={'default_permissions': (), 'managed': False, 'permissions': (('landingpage_right', 'Right to view landingpage'), ('health_app', 'Right to user Health App'))},
        ),
    ]