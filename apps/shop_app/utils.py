from django.db.models import When, Case

from . import models
from shop import settings

import json


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        auth = self.request.user.is_authenticated
        context['auth'] = auth
        return context

def get_hit_products(category):
    return category.products.filter(hit=True)

def redis_views_categories(element_id, key=settings.CATEGORY_REDIS_KEY):
    element_id = str(element_id)
    if not settings.r.exists(key):
        settings.r.set(key, json.dumps({}))
    els = json.loads(settings.r.get(key))
    if element_id not in els.keys():
        els[element_id] = 0
    els[element_id] += 1
    settings.r.set(key, json.dumps(els))

def redis_views_products(category_id, element_id, key=settings.PRODUCT_REDIS_KEY):
    category_id, element_id = str(category_id), str(element_id)
    if not settings.r.exists(key):
        settings.r.set(key, json.dumps({}))
    els = json.loads(settings.r.get(key))
    if category_id not in els.keys():
        els[category_id] = {element_id: 1}
        settings.r.set(key, json.dumps(els))
        return None
    if element_id not in els[category_id].keys():
        els[category_id][element_id] = 1
        settings.r.set(key, json.dumps(els))
        return None
    els[category_id][element_id] += 1
    settings.r.set(key, json.dumps(els))


def get_populated_cats(limit=3):
    cats = json.loads(settings.r.get(settings.CATEGORY_REDIS_KEY)).items()
    if len(cats) < limit: limit = len(cats)
    cat_ids = list(map(lambda x: x[0], sorted(cats, key=lambda x: x[1], reverse=True)[:limit]))
    categories = models.Category.objects.filter(id__in=cat_ids)
    cats_positions = [When(id=cat_id, then=pos) for pos, cat_id in enumerate(cat_ids)]
    return categories.annotate(position=Case(*cats_positions, default=len(cat_ids))).order_by('position')

def get_populated_products(category, limit=5):
    products = json.loads(settings.r.get(settings.PRODUCT_REDIS_KEY))[str(category.pk)]
    if len(products) < limit: limit = len(products)
    products_ids = map(lambda x: x[0], sorted(products.items(), key=lambda x: x[1], reverse=True)[:limit])
    return category.products.filter(id__in=products_ids)