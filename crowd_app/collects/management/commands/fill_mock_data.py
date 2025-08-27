# noinspection PyUnresolvedReferences
from django.core.management.base import BaseCommand
# noinspection PyUnresolvedReferences
from django.contrib.auth import get_user_model
# noinspection PyUnresolvedReferences
from collects.models import Collect, Occasion
# noinspection PyUnresolvedReferences
from payments.models import Payment
# noinspection PyUnresolvedReferences
from django.utils import timezone
from datetime import timedelta
import random
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Fill database with mock data'

    def handle(self, *args, **options):
        self.stdout.write('Creating mock data...')

        # Создаем пользователей
        users = []
        for i in range(1, 101):
            user, created = User.objects.get_or_create(
                username=f'user{i}',
                defaults={
                    'email': f'user{i}@example.com',
                    'first_name': f'User{i}',
                    'last_name': f'Lastname{i}',
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)

        # Создаем сборы
        collects = []
        occasions = [occ[0] for occ in Occasion.choices]

        for i in range(1, 201):
            author = random.choice(users)
            end_date = timezone.now() + timedelta(days=random.randint(1, 365))

            collect = Collect.objects.create(
                author=author,
                title=f'Сбор #{i} - {random.choice(occasions)}',
                occasion=random.choice(occasions),
                description=f'Описание для сбора #{i}',
                target_amount=Decimal(random.randint(1000, 100000)),
                end_datetime=end_date
            )
            collects.append(collect)

        # Создаем платежи
        for i in range(1, 5001):
            user = random.choice(users)
            collect = random.choice(collects)

            payment = Payment.objects.create(
                user=user,
                collect=collect,
                amount=Decimal(random.randint(50, 5000)),
                comment=f'Пожертвование #{i}',
                is_anonymous=random.choice([True, False])
            )

            # Обновляем текущую сумму сбора
            collect.current_amount += payment.amount
            collect.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created: {len(users)} users, '
                f'{len(collects)} collects, 5000 payments'
            )
        )