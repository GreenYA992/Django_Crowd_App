# noinspection PyUnresolvedReferences
from django.test import TestCase
# noinspection PyUnresolvedReferences
from django.urls import reverse
# noinspection PyUnresolvedReferences
from rest_framework.test import APITestCase, APIClient
# noinspection PyUnresolvedReferences
from rest_framework import status
from .models import Collect
# noinspection PyUnresolvedReferences
from django.contrib.auth import get_user_model
# noinspection PyUnresolvedReferences
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class CollectModelTest(TestCase):
    def test_create_collect(self):
        user = User.objects.create_user('testuser', 'test@example.com', 'password')
        collect = Collect.objects.create(
            author=user,
            title='Test Collect',
            occasion='birthday',
            description='Test description',
            target_amount=10000,
            end_datetime=timezone.now() + timedelta(days=30)
        )
        self.assertEqual(str(collect), 'Test Collect')


class CollectAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.collect_data = {
            'title': 'API Test Collect',
            'occasion': 'birthday',
            'description': 'API test description',
            'target_amount': 15000,
            'end_datetime': (timezone.now() + timedelta(days=30)).isoformat()
        }

    def test_create_collect_via_api(self):
        url = reverse('collect-list')
        response = self.client.post(url, self.collect_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Collect.objects.count(), 1)
        self.assertEqual(Collect.objects.get().title, 'API Test Collect')

    def test_get_collects_list(self):
        Collect.objects.create(
            author=self.user,
            title='Test Collect 1',
            occasion='wedding',
            description='Test 1',
            target_amount=5000,
            end_datetime=timezone.now() + timedelta(days=10)
        )

        url = reverse('collect-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_collect_validation(self):
        invalid_data = self.collect_data.copy()
        invalid_data['end_datetime'] = (timezone.now() - timedelta(days=1)).isoformat()

        url = reverse('collect-list')
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
