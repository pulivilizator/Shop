from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Coupon
from ..cart.cart import Cart


@require_POST
def coupon_apply(request, coupon_code):
    now = timezone.now()
    try:
        coupon = Coupon.objects.get(
            code__iexact=coupon_code,
            valid_from__lte=now,
            valid_to__gte=now,
            active=True
        )
    except Coupon.DoesNotExist:
        print('NET')
        return JsonResponse({'error': 'Купон не найден'}, status=404)

    request.session['coupon_id'] = coupon.id
    cart = Cart(request)
    print(cart.coupon)
    return JsonResponse({'success': True,
                         'cart_total_price': cart.get_discount_total_price(),
                         'cart_discount': cart.get_discount()})