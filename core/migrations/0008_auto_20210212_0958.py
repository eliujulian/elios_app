# Generated by Django 3.1.5 on 2021-02-12 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210207_1338'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='permissionregister',
            options={'default_permissions': (), 'managed': False, 'permissions': (('landingpage_right', 'Right to view landingpage'), ('health_app', 'Right to user Health App'), ('personality_app', 'Use Personality App'))},
        ),
    ]
