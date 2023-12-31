from django.urls import path, include

from project_drf.apps import ProjectDrfConfig
from rest_framework.routers import DefaultRouter

from project_drf.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentsListAPIView, SubscriptionCreateAPIView, \
    SubscriptionDestroyAPIView, PaymentsCreateAPIView, GetPaymentView

app_name = ProjectDrfConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('payments/', PaymentsListAPIView.as_view(), name='payments-list'),
    path('course/<int:pk>/subscribe/', SubscriptionCreateAPIView.as_view(), name='subscription-create'),
    path('course/<int:pk>/unsubscribe/', SubscriptionDestroyAPIView.as_view(), name='subscription-delete'),
    path('course/<int:pk>/payment/', PaymentsCreateAPIView.as_view(), name='payment-create'),
    path('payments/<int:pk>/', GetPaymentView.as_view(), name='payment-get'),
]
