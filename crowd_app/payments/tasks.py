# noinspection PyUnresolvedReferences
from celery import shared_task
# noinspection PyUnresolvedReferences
from django.core.mail import send_mail
# noinspection PyUnresolvedReferences
from django.conf import settings
from .models import Payment


@shared_task
def send_payment_created_email(payment_id):
    try:
        payment = Payment.objects.select_related('user', 'collect').get(id=payment_id)
        subject = 'Спасибо за ваше пожертвование!'
        message = f'''
        Здравствуйте, {payment.user.get_full_name()}!

        Благодарим вас за пожертвование в размере {payment.amount} руб.
        в сбор "{payment.collect.title}".

        Ваша поддержка очень важна!
        '''
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [payment.user.email],
            fail_silently=False,
        )
    except Payment.DoesNotExist:
        pass