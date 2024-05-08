from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models
from . import utils


@receiver(post_save, sender=models.Category)
def create_category_views(**kwargs):
    instance = kwargs['instance']
    utils.redis_views_categories(element_id=instance.pk)

@receiver(post_save, sender=models.Product)
def create_category_views(**kwargs):
    instance = kwargs['instance']
    utils.redis_views_products(category_id=instance.subcategory.pk, element_id=instance.pk)