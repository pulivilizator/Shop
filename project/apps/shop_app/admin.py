from django.contrib import admin

from . import models




@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'created']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'category']


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'subcategory', 'slug', 'imagine',
                    'price', 'available', 'hit', 'created', 'update']
    list_filter = ['available', 'created', 'hit', 'update', 'price']
    list_editable = ['price', 'available', 'hit']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.PropertyGroup)
class PropertyGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name', 'category']


@admin.register(models.Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['group', 'type', 'value']


@admin.register(models.PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'subcategory_field']
    list_filter = ['name']


@admin.register(models.PropertyValue)
class PropertyValueAdmin(admin.ModelAdmin):
    list_display = ['value']
    list_filter = ['value']
