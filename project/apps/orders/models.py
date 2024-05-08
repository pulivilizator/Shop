from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from apps.coupons.models import Coupon
from apps.shop_app.models import Product


class Country(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'country'
        verbose_name_plural = 'countries'

    def __str__(self):
        return self.name


class DeliveryMethod(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}|{self.price}'


class PaymentMethod(models.Model):
    name = models.CharField(max_length=150)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,
                             null=True, related_name='orders')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    email = models.EmailField()
    country = models.ForeignKey(Country, related_name='orders',
                                on_delete=models.SET_NULL, null=True)
    delivery_method = models.ForeignKey(DeliveryMethod, related_name='orders',
                                        on_delete=models.SET_NULL, null=True)
    payment_method = models.ForeignKey(PaymentMethod, related_name='orders',
                                       on_delete=models.SET_NULL, null=True)
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    stripe_id = models.CharField(max_length=250, blank=True)
    coupon = models.ForeignKey(Coupon, related_name='orders',
                               on_delete=models.SET_NULL, null=True)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                          MaxValueValidator(
                                                              100)])
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f'Order {self.id}'

    def get_total_price_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        if self.discount:
            return (self.get_total_price_before_discount() * (
                        self.discount / Decimal(100))).quantize(
                Decimal('0.00'))
        return Decimal(0)

    def get_total_price(self):
        total_price = self.get_total_price_before_discount() - self.get_discount()
        if self.delivery_method.price:
            return total_price + self.delivery_method.price
        return total_price

    def get_stripe_url(self):
        if not self.stripe_id:
            return ''

        if '_test_' in settings.STRIPE_SECRET_KEY:
            path = '/test/'

        else:
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'

    def get_absolute_url(self):
        username = 'anonymous'
        if self.user:
            username = self.user.username
        return reverse('order:detail_order',
                       kwargs={'order_id': self.id, 'username': username})


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Order {self.id}'

    def get_cost(self):
        return self.price * self.quantity
