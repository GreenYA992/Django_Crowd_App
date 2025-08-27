# noinspection PyUnresolvedReferences
from django.db import models
# noinspection PyUnresolvedReferences
from django.contrib.auth import get_user_model
# noinspection PyUnresolvedReferences
from django.core.validators import MinValueValidator
# noinspection PyUnresolvedReferences
from collects.models import Collect
# noinspection PyUnresolvedReferences
from django.core.exceptions import ValidationError

User = get_user_model()

class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    collect = models.ForeignKey(
        Collect,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )
    comment = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} - {self.amount}'

    def clean(self):
        if self.amount <= 0:
            raise ValidationError('Сумма платежа должна быть положительной')
        if not self.collect.is_active:
            raise ValidationError('Нельзя сделать платеж в завершенный сбор')
