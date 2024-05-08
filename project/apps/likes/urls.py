from django.urls import path

from . import views

app_name = 'likes'

urlpatterns = [
    path('add_to_likes/<int:product_id>/', views.add_to_likes, name='add_to_likes'),
    path('remove_from_likes/<int:product_id>/', views.remove_from_likes, name='remove_from_likes'),
    path('clear_likes/', views.clear_likes, name='clear_likes'),
    path('likes/', views.LikesView.as_view(), name='likes'),

]