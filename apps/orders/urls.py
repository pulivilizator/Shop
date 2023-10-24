from django.urls import path

from . import views

app_name = 'order'

urlpatterns = [
    path('create_order/', views.CreateOrderView.as_view(), name='create_order'),
    path('detail_order/<slug:username>/<int:order_id>', views.DetailOrderView.as_view(), name='detail_order'),
]