import requests
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from project_drf.models import Course, Lesson, Payments, Subscription
from project_drf.pagination import ListPagination
from project_drf.permissions import IsOwner, IsStaff
from project_drf.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, SubscriptionSerializer
from project_drf.services import perform_payment, get_payment


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = ListPagination

    def get_permissions(self):
        permission_classes = [AllowAny]
        if self.action == 'create':
            permission_classes = [~ IsStaff]
        elif self.action == 'list':
            permission_classes = []
        elif self.action == 'retrieve':
            permission_classes = [IsOwner]
        elif self.action == 'update':
            permission_classes = [IsStaff | IsOwner]
        elif self.action == 'destroy':
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~ IsStaff]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = ListPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsStaff | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'online_payment', 'cash_payment',)
    ordering_fields = ('date',)


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer, **kwargs):
        payment = serializer.save()
        payment.user = self.request.user
        course_pk = self.kwargs.get('pk')
        payment.course = Course.objects.get(pk=course_pk)
        payment.total = payment.course.price
        payment.online_payment = True
        stripe_payment = perform_payment(payment.total)
        payment.stripe_id = stripe_payment["id"]
        payment.save()


class GetPaymentView(APIView):
    def get(self, request, *args, **kwargs):
        payment = Payments.objects.get(pk=self.kwargs.get('pk'))
        response = get_payment(payment.stripe_id)

        return response


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def perform_create(self, serializer, **kwargs):
        subscription = serializer.save()
        subscription.user = self.request.user
        pk = self.kwargs.get('pk')
        subscription.course = Course.objects.get(pk=pk)
        subscription.save()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

