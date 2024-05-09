from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Модель категорий"""
    category = models.ForeignKey('self', related_name='subcategories',
                                 on_delete=models.CASCADE, blank=True,
                                 null=True,
                                 limit_choices_to={'category__isnull': True})
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    imagine = models.ImageField(upload_to='subcategory/%Y/%m/%d', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)

        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['-created'])
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category', kwargs={'category_slug': self.slug})


class Product(models.Model):
    """Модель товара"""
    subcategory = models.ForeignKey(Category, related_name='products',
                                    on_delete=models.CASCADE,
                                    limit_choices_to={
                                        'category__isnull': False})
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    imagine = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    hit = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
            models.Index(fields=['subcategory'])
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product', kwargs={'product_id': self.pk,
                                               'product_slug': self.slug})


class PropertyGroup(models.Model):
    """Группы свойств продуктов"""
    category = models.ManyToManyField(Category, related_name='groups',
                                      blank=True)
    name = models.CharField(max_length=200)

    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name


class PropertyType(models.Model):
    """Модель свойств продукта"""
    subcategory_field = models.BooleanField(default=False)
    name = models.CharField(max_length=200)

    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name


class PropertyValue(models.Model):
    """Модель значения свойства"""
    value = models.CharField(max_length=200)

    class Meta:
        indexes = [
            models.Index(fields=['value'])
        ]

    def __str__(self):
        return self.value

class Property(models.Model):
    """Модель для объединения свойства и значения"""
    group = models.ForeignKey(PropertyGroup, related_name='properties',
                              on_delete=models.CASCADE, blank=True)
    product = models.ManyToManyField(Product, related_name='properties', blank=True)
    type = models.ForeignKey(PropertyType, related_name='properties',
                             on_delete=models.CASCADE, blank=True)
    value = models.ForeignKey(PropertyValue, related_name='properties',
                              on_delete=models.CASCADE, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['type', 'value']),
        ]
        verbose_name = 'property'
        verbose_name_plural = 'properties'

    def __str__(self):
        return f'{self.type}: {self.value}'
