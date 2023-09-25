from django.contrib import admin
from django.db import models

from django_json_widget.widgets import JSONEditorWidget

from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'created']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'category']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'subcategory', 'slug', 'imagine',
                    'price', 'available', 'hit', 'created', 'update']
    list_filter = ['available', 'created', 'hit', 'update', 'price']
    list_editable = ['price', 'available', 'hit']
    search_fields = ['category', 'name']
    prepopulated_fields = {'slug': ('name', )}

@admin.register(PropertyGroup)
class PropertyGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name', 'category']

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['group', 'product', 'type', 'value']

@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'subcategory_field']
    list_filter = ['name']

@admin.register(PropertyValue)
class PropertyValueAdmin(admin.ModelAdmin):
    list_display = ['value']
    list_filter = ['value']
