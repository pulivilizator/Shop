from celery import shared_task
from django.core.mail import send_mail

from . import models


@shared_task
def order_created(order_id):
    order = models.Order.objects.get(id=order_id)
    subject = f'Заказ №{order.id} создан'
    message = (f'Здравствуйте {order.first_name} {order.last_name},\n\n'
               f'Вы успешно оформили заказ в магазине ComputerShop\n'
               f'Ваш номер заказа: {order_id}\n'
               f'Ссылка на Ваш заказ: {order.get_absolute_url()}')
    mail_sent = send_mail(subject, message, 'DmitriyDmGora@gmail.com', [order.email])
    return mail_sent
