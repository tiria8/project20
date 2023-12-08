from rest_framework import serializers

from project_drf.models import Course, Lesson, Payments, Subscription
from project_drf.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [UrlValidator(field='url')]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lesson_count(self, instance):
        return instance.lesson_set.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
