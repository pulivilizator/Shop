from django.urls import path

from . import  views

app_name = 'shop'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('<slug:category_slug>', views.CategoryPage.as_view(), name='category'),
    path('<slug:slug>/<slug:category_slug>', views.SubcategoryPage.as_view(), name='subcategory'),
    path('product/<int:product_id>/<slug:product_slug>', views.ProductPage.as_view(), name='product'),

]