from django.core.management import BaseCommand

from project_drf.models import Payments, Course, Lesson


class Command(BaseCommand):

    def handle(self, *args, **options):
        payments_info = [
            {'course': Course.objects.get(pk=2), 'total': 10000, 'online_payment': True},
            {'course': Course.objects.get(pk=1), 'total': 5500, 'cash_payment': True},
            {'lesson': Lesson.objects.get(pk=2), 'total': 500, 'online_payment': True},
            {'lesson': Lesson.objects.get(pk=3), 'total': 2300, 'cash_payment': True}
        ]

        for payment in payments_info:
            Payments.objects.create(**payment)
