import codecs
import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from . import models


def order_stripe_payment(obj):
    if obj.stripe_id:
        url = obj.get_stripe_url()
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''
order_stripe_payment.short_description = 'Stripe payment'

def order_details(obj):
    url = obj.get_absolute_url()
    return mark_safe(f'<a href="{url}" target="_blank">Details from order №{obj.id}</a>')
order_details.short_description = 'Order details'

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    raw_id_fields = ('product',)


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename="{opts.verbose_name}.csv"'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response, delimiter=';', quoting=csv.QUOTE_ALL)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        writer.writerow(
            [getattr(obj, field.name).strftime('%d/%m/%Y') if isinstance(getattr(obj, field.name), datetime.datetime) else getattr(obj, field.name) for field in fields]
        )
    return response
export_to_csv.short_description = 'Export to CSV'

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'country',
                    'region', 'city', 'address', 'postal_code', 'paid',
                    order_stripe_payment, order_details, 'created', 'updated')
    list_filter = ('country', 'created', 'updated', 'paid')
    inlines = [OrderItemInline]
    actions = [export_to_csv]


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
