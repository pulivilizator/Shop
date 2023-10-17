from django.contrib import admin

from . import models


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    raw_id_fields = ('product',)


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'country',
                    'region', 'city', 'address', 'postal_code', 'paid',
                    'created', 'updated')
    list_filter = ('country', 'created', 'updated', 'paid')
    inlines = [OrderItemInline]

@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    list_filter = ('active',)

@admin.register(models.DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'active', 'created', 'updated')
    list_filter = ('active',)

@admin.register(models.PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'created', 'updated',)
    list_filter = ('active',)