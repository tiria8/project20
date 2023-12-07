from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from project_drf.models import Course, Lesson, Payments, Subscription
from project_drf.pagination import ListPagination
from project_drf.permissions import IsOwner, IsStaff
from project_drf.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, SubscriptionSerializer


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
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
