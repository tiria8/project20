from django.contrib import admin

from project_drf.models import Course, Lesson, Subscription, Payments


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'owner',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('course', 'user',)

@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Payments._meta.get_fields()]

