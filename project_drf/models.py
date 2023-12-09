from django.db import models

from config import settings

from datetime import date

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    course_preview = models.ImageField(upload_to='project/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='создатель')
    price = models.PositiveIntegerField(default=500, verbose_name='цена')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курсы'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    lesson_preview = models.ImageField(upload_to='project/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    url = models.URLField(max_length=300, verbose_name='ссылка', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='создатель')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='пользователь')
    date = models.DateField(default=date.today, verbose_name='дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE)
    total = models.PositiveIntegerField(verbose_name='сумма оплаты', **NULLABLE)
    online_payment = models.BooleanField(verbose_name='оплата переводом на счет', default=False, **NULLABLE)
    cash_payment = models.BooleanField(verbose_name='оплата наличными', default=False, **NULLABLE)
    stripe_id = models.CharField(max_length=250, verbose_name='Stripe ID', **NULLABLE)


class Subscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, ** NULLABLE, verbose_name='пользователь')

    def __str__(self):
        return f'Курс: {self.course} - пользователь {self.user}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
