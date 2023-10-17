from django.core.mail import send_mail
from django.conf import settings

from . import models

from celery import shared_task


@shared_task
def order_created(order_id):
    print('qweyy3312q')
    order = models.Order.objects.get(id=order_id)
    subject = f'Заказ №{order.id} создан'
    message = (f'Здравствуйте {order.first_name} {order.last_name},\n\n'
               f'Вы успешно оформили заказ в магазине ComputerShop'
               f'Ваш номер заказа: {order_id}')
    mail_sent = send_mail(subject, message, 'DmitriyDmGora@gmail.com', [order.email])
    return mail_sent