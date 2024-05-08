from django.urls import path

from . import views

app_name = 'coupons'

urlpatterns = [
    path('apply/<slug:coupon_code>/', views.coupon_apply, name='coupon_apply'),
]