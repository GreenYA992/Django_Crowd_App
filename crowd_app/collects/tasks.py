# noinspection PyUnresolvedReferences
from celery import shared_task
# noinspection PyUnresolvedReferences
from django.core.mail import send_mail
# noinspection PyUnresolvedReferences
from django.conf import settings
from .models import Collect


@shared_task
def send_collect_created_email(collect_id):
    try:
        collect = Collect.objects.get(id=collect_id)
        subject = 'Ваш сбор успешно создан!'
        message = f'''
        Здравствуйте, {collect.author.get_full_name()}!

        Ваш сбор "{collect.title}" успешно создан.
        Цель: {collect.target_amount or "Бесконечный сбор"}
        Завершение: {collect.end_datetime}

        Ссылка на сбор: {settings.FRONTEND_URL}/collects/{collect.id}
        '''
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [collect.author.email],
            fail_silently=False,
        )
    except Collect.DoesNotExist:
        pass