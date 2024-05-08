from decimal import Decimal as D

import stripe
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404

from apps.orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

        session_data = {
            'mode': 'payment',
            'client_reference_id': order_id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': [],
        }

        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * D('100')),
                    'currency': 'rub',
                    'product_data': {
                        'name': item.product.name
                    },
                },
                'quantity': item.quantity,
            })
        if isinstance(order.delivery_method.price, (int, float, D)):
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(order.delivery_method.price * D('100')),
                    'currency': 'rub',
                    'product_data': {
                        'name': order.delivery_method.name
                    },
                },
                'quantity': 1,
            })

        if order.coupon:
            stripe_coupon = stripe.Coupon.create(
                name=order.coupon.code,
                percent_off=order.discount,
                duration='once'
            )
            session_data['discounts'] = [{'coupon': stripe_coupon.id}]
        session = stripe.checkout.Session.create(**session_data)

        return redirect(session.url, code=303)
    else:
        return render(request,
                      'orders/detail_order.html',
                      {'title': f'Заказ №{order_id}',
                       'buy': True,
                       'order_id': order_id,
                       'products': order.items.all().select_related('product'),
                       'total_price': order.get_total_price()})


def payment_completed(request):
    return render(request, 'payment/completed.html',
                  {'title': 'Заказ оплачен'})


def payment_canceled(request):
    return render(request, 'payment/canceled.html',
                  {'title': 'Ошибка оплаты заказа'})
