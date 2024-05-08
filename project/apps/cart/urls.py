from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('delete_from_cart/<int:product_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),

    path('cart', views.CartView.as_view(), name='cart'),

]