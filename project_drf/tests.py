from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from project_drf.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='test', password='test')
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='test_course',
            description='test_course',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            title='test_lesson',
            description='test_l',
            course=self.course,
            url='http://www.youtube.com/test_l',
            owner=self.user
        )

    def test_list(self):
        """Test for getting lessons' list"""
        response = self.client.get(
            reverse('project_drf:lesson-list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 1,
             'next': None,
             'previous': None,
             'results': [
                 {'id': self.lesson.pk,
                  'title': self.lesson.title,
                  'lesson_preview': None,
                  'description': self.lesson.description,
                  'url': self.lesson.url,
                  'course': self.course.pk,
                  'owner': self.user.pk
                  }
             ]
             }
        )

    def test_retrieve(self):
        """Test for getting lesson details"""
        response = self.client.get(
            reverse('project_drf:lesson-get', kwargs={'pk': self.lesson.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.lesson.pk,
             'title': self.lesson.title,
             'lesson_preview': None,
             'description': self.lesson.description,
             'url': self.lesson.url,
             'course': self.course.pk,
             'owner': self.user.pk
             }
        )

    def test_create(self):
        """Test for creating a lesson"""
        data = {
            'title': 'test_lesson',
            'description': 'test_l',
            'url': 'http://www.youtube.com/test_l',
            'course': self.course.pk,
            'owner': self.user.pk
        }

        response = self.client.post(
            reverse('project_drf:lesson-create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': 2,
             'title': 'test_lesson',
             'lesson_preview': None,
             'description': 'test_l',
             'url': 'http://www.youtube.com/test_l',
             'course': self.course.pk,
             'owner': self.user.pk
             }

        )

    def test_update(self):
        """Test for updating the lesson"""
        data = {
            'title': 'test_lesson_upd',
            'description': self.lesson.description,
            'url': self.lesson.url,
            'course': self.course.pk,
            'owner': self.user.pk
        }

        response = self.client.patch(
            reverse('project_drf:lesson-update', kwargs={'pk': self.lesson.pk}),
            data=data
        )

        print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.lesson.pk,
             'title': 'test_lesson_upd',
             'lesson_preview': None,
             'description': self.lesson.description,
             'url': self.lesson.url,
             'course': self.course.pk,
             'owner': self.user.pk
             }
        )

    def test_delete(self):
        """Test for deleting the lesson"""
        response = self.client.delete(
            reverse('project_drf:lesson-delete', kwargs={'pk': self.lesson.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='test', password='test')
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='test_course',
            description='test_course',
            owner=self.user
        )

    def test_create(self):
        """Test for creating a course subscription"""
        subscription = {
            "user": self.user.pk,
            "course": self.course.pk
        }

        response = self.client.post(
            reverse('project_drf:subscription-create', kwargs={'pk': self.course.pk}),
            data=subscription
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_delete(self):
        """Test for removing a course subscription"""

        course = Subscription.objects.create(
            user=self.user,
            course=self.course
        )

        response = self.client.delete(
            reverse('project_drf:subscription-delete', kwargs={'pk': course.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
