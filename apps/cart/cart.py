from django.conf import settings

from apps.shop_app import models
from apps.coupons.models import Coupon

from decimal import Decimal as D

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity

        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def delete(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= quantity

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = models.Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = D(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_product_price(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            return self.cart[product_id]['quantity'] * D(self.cart[product_id]['price'])


    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        self.cart = self.session[settings.CART_SESSION_ID] = {}
        self.save()

    def get_total_price(self):
        return sum(D(item['price']) * item['quantity']
                   for item in self.cart.values())

    def get_discount(self):
        if self.coupon:
            return ((self.coupon.discount / D(100)) * self.get_total_price()).quantize(D("0.00"))
        return D(0)

    def get_discount_total_price(self):
        return (self.get_total_price() - self.get_discount()).quantize(D("0.00"))

    def count(self):
        return self.__len__()

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
