# noinspection PyUnresolvedReferences
from rest_framework import viewsets, status, permissions
# noinspection PyUnresolvedReferences
from rest_framework.response import Response
# noinspection PyUnresolvedReferences
from rest_framework.permissions import IsAuthenticated
# noinspection PyUnresolvedReferences
from django.db import transaction
from .models import Payment
from .serializers import PaymentSerializer
# noinspection PyUnresolvedReferences
from .tasks import send_payment_created_email
# noinspection PyUnresolvedReferences
from collects.models import Collect
# noinspection PyUnresolvedReferences
from django.contrib.auth import get_user_model


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.AllowAny]  # Для тестирования

    def get_queryset(self):
        return Payment.objects.all()

    def perform_create(self, serializer):
        # Для тестирования без аутентификации
        User = get_user_model()
        first_user = User.objects.first()
        first_collect = Collect.objects.first()
        payment = serializer.save(user=first_user, collect=first_collect)
        # Обновляем сумму сбора
        payment.collect.current_amount += payment.amount
        payment.collect.save()
