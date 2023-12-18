from datetime import date, timedelta

from celery import shared_task
from django.core.mail import send_mail

from project_drf.models import Course, Subscription
from users.models import User


@shared_task
def subscriber_notice(course_id):
    course = Course.objects.get(pk=course_id)

    subscriptions = Subscription.objects.filter(course=course_id)

    if subscriptions:
        for subscription in subscriptions:
            send_mail(
                subject=f'Обновление курса: {course.course_title}',
                message=f'Привет, {subscription.user}! Курс, на который ты подписан, недавно был обновлен.',
                from_email='dasha@mail.com',
                recipient_list=[subscription.user.email]
            )
            print(f'Письмо отправлено на {subscription.user.email}')


def block_user():
    users = User.objects.all()

    for user in users:
        if date.today - user.last_login >= timedelta(days=30):
            user.is_active = False
            user.save()
