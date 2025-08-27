# noinspection PyUnresolvedReferences
from django.test import TestCase
# noinspection PyUnresolvedReferences
from django.urls import reverse
# noinspection PyUnresolvedReferences
from rest_framework.test import APITestCase, APIClient
# noinspection PyUnresolvedReferences
from rest_framework import status
from .models import Payment
# noinspection PyUnresolvedReferences
from collects.models import Collect
# noinspection PyUnresolvedReferences
from django.contrib.auth import get_user_model
# noinspection PyUnresolvedReferences
from django.utils import timezone
from decimal import Decimal

User = get_user_model()


class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.collect = Collect.objects.create(
            author=self.user,
            title='Test Collect',
            occasion='birthday',
            description='Test',
            target_amount=Decimal('10000.00'),
            end_datetime=timezone.now() + timezone.timedelta(days=30)
        )

    def test_create_payment(self):
        payment = Payment.objects.create(
            user=self.user,
            collect=self.collect,
            amount=Decimal('1000.00'),
            comment='Test payment'
        )

        self.collect.refresh_from_db()

        self.assertEqual(payment.amount, Decimal('1000.00'))
        self.assertEqual(self.collect.current_amount, Decimal('1000.00'))


class PaymentAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.collect = Collect.objects.create(
            author=self.user,
            title='Test Collect',
            occasion='birthday',
            description='Test',
            target_amount=Decimal('1000.00'),
            end_datetime=timezone.now() + timezone.timedelta(days=30),
            current_amount = Decimal('0.00')
        )

        self.payment_data = {
            'collect': self.collect.id,
            'amount': 500,
            'comment': 'Test payment via API',
            'is_anonymous': False
        }

    def test_create_payment_via_api(self):
        # Убедимся, что сбор начинается с 0
        url = reverse('payment-list')
        response = self.client.post(url, self.payment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 1)

        # Получаем платеж и проверяем
        payment = Payment.objects.first()
        self.assertEqual(payment.amount, Decimal('500.00'))

        # Проверяем, что сумма сбора обновилась
        self.collect.refresh_from_db()
        self.assertEqual(self.collect.current_amount, Decimal('500.00'))

    def test_payment_validation(self):
        invalid_data = self.payment_data.copy()
        invalid_data['amount'] = -100  # Отрицательная сумма

        url = reverse('payment-list')
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
