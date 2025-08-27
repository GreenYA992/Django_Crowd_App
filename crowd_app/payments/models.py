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
from decimal import Decimal

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
        validators=[MinValueValidator(Decimal(1))]
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

    def save(self, *args, **kwargs):
        # Если это новая запись (не обновление)
        is_new = self._state.adding

        # Сначала сохраняем платеж
        super().save(*args, **kwargs)

        # Если это новый платеж - обновляем сумму сбора
        if is_new:
            self.collect.current_amount += self.amount
            self.collect.save()
