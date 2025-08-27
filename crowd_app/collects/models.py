# noinspection PyUnresolvedReferences
from django.db import models
# noinspection PyUnresolvedReferences
from django.contrib.auth import get_user_model
# noinspection PyUnresolvedReferences
from django.core.validators import MinValueValidator
# noinspection PyUnresolvedReferences
from django.utils import timezone
# noinspection PyUnresolvedReferences
from django.core.exceptions import ValidationError
from decimal import Decimal

User = get_user_model()

def validate_future_date(value):
    """Валидатор для проверки, что дата в будущем"""
    if value <= timezone.now():
        raise ValidationError('Дата завершения должна быть в будущем')

class Occasion(models.TextChoices):
    BIRTHDAY = 'birthday', 'День рождения'
    WEDDING = 'wedding', 'Свадьба'
    MEDICAL = 'medical', 'Лечение'
    EDUCATION = 'education', 'Образование'
    CHARITY = 'charity', 'Благотворительность'
    OTHER = 'other', 'Другое'

class Collect(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='collects'
    )
    title = models.CharField(max_length=200)
    occasion = models.CharField(
        max_length=20,
        choices=Occasion.choices,
        default=Occasion.OTHER
    )
    description = models.TextField()
    target_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0'))]
    )
    current_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0'))]
    )
    cover_image = models.ImageField(
        upload_to='collects/covers/',
        null=True,
        blank=True
    )
    end_datetime = models.DateTimeField(
        validators=[validate_future_date],
        help_text='Дата и время завершения сбора'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_active(self):
        return timezone.now() < self.end_datetime

    @property
    def progress_percentage(self):
        if self.target_amount and self.target_amount > 0:
            return (self.current_amount / self.target_amount) * 100
        return 0

    def clean(self):
        if self.target_amount is not None and self.target_amount <= 0:
            raise ValidationError('Целевая сумма должна быть положительной')
        if self.end_datetime <= timezone.now():
            raise ValidationError('Дата завершения должна быть в будущем')
