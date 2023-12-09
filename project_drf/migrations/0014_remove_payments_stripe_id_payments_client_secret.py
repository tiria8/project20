# Generated by Django 4.2.7 on 2023-12-09 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_drf', '0013_rename_stipe_id_payments_stripe_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payments',
            name='stripe_id',
        ),
        migrations.AddField(
            model_name='payments',
            name='client_secret',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Client secret'),
        ),
    ]