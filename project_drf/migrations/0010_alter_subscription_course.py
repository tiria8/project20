# Generated by Django 4.2.7 on 2023-12-07 21:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_drf', '0009_alter_subscription_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project_drf.course', verbose_name='курс'),
        ),
    ]