from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('create_order/', views.CreateOrderView.as_view(), name='create_order'),
]