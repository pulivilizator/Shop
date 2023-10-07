from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import generic

from .cart import Cart
from apps.shop_app import models as shop_app_models
from apps.shop_app import utils

from decimal import Decimal as D

def add_to_cart(request, product_id, quantity=1):
    """Добавляет указанное количество товаров"""
    cart = Cart(request)
    product = get_object_or_404(shop_app_models.Product, id=product_id)
    cart.add(product, quantity=quantity)
    return JsonResponse({'success': True,
                         'new_quantity': cart.cart[str(product_id)]['quantity'],
                         'total_price': cart.get_product_price(product_id),
                         'cart_total_price': cart.get_total_price()})


def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(shop_app_models.Product, id=product_id)
    cart.remove(product)
    return JsonResponse({'success': True,
                         'cart_total_price': cart.get_total_price()})

def delete_from_cart(request, product_id, quantity=1):
    """Вычитает указанное количество товара"""
    cart = Cart(request)
    product = get_object_or_404(shop_app_models.Product, id=product_id)
    cart.delete(product, quantity=quantity)
    if cart.cart[str(product_id)] < 1: remove_from_cart(request, product_id)
    return JsonResponse({'success': True,
                         'new_quantity': cart.cart[str(product_id)]['quantity'],
                         'total_price': cart.get_product_price(product_id),
                         'cart_total_price': cart.get_total_price()})

def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return JsonResponse({'success': True})

class CartView(utils.DataMixin, generic.ListView):
    template_name = 'cart/cart.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        up_context = self.get_user_context(title='Корзина')
        context.update(up_context)

        return context

    def get_queryset(self):
        cart = Cart(self.request)
        prods = shop_app_models.Product.objects.filter(id__in=cart.cart.keys())
        for p in prods:
            p.quantity = cart.cart[str(p.id)]['quantity']
            if p.quantity < 1: cart.remove(p)
            p.total_price = D(cart.cart[str(p.id)]['price']) * cart.cart[str(p.id)]['quantity']
        return prods
