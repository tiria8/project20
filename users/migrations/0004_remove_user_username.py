# Generated by Django 4.2.7 on 2023-12-01 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
