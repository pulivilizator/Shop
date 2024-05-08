import json

import redis
import requests
from django.conf import settings
from django.db.models import When, Case

from . import models

CATEGORY_REDIS_KEY = 'category:views'
PRODUCT_REDIS_KEY = 'product:views'

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB, )


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        auth = self.request.user.is_authenticated
        context['auth'] = auth
        return context


def get_hit_products(category):
    return category.products.filter(hit=True)


def redis_views_categories(element_id, key=CATEGORY_REDIS_KEY):
    element_id = str(element_id)
    if not r.exists(key):
        r.set(key, json.dumps({}))
    els = json.loads(r.get(key))
    if element_id not in els.keys():
        els[element_id] = 0
    els[element_id] += 1
    r.set(key, json.dumps(els))


def redis_views_products(category_id, element_id, key=PRODUCT_REDIS_KEY):
    category_id, element_id = str(category_id), str(element_id)
    if not r.exists(key):
        r.set(key, json.dumps({}))
    els = json.loads(r.get(key))
    if category_id not in els.keys():
        els[category_id] = {element_id: 1}
        r.set(key, json.dumps(els))
        return None
    if element_id not in els[category_id].keys():
        els[category_id][element_id] = 1
        r.set(key, json.dumps(els))
        return None
    els[category_id][element_id] += 1
    r.set(key, json.dumps(els))


def get_populated_cats(limit=3):
    cats = json.loads(r.get(CATEGORY_REDIS_KEY)).items()
    if len(cats) < limit: limit = len(cats)
    cat_ids = list(map(lambda x: x[0], sorted(cats, key=lambda x: x[1], reverse=True)[:limit]))
    categories = models.Category.objects.filter(id__in=cat_ids, category__isnull=False).select_related('category')
    cats_positions = [When(id=cat_id, then=pos) for pos, cat_id in enumerate(cat_ids)]
    return categories.annotate(position=Case(*cats_positions, default=len(cat_ids))).order_by('position')


def get_populated_products(category, limit=5):
    if category.category is not None:
        products = json.loads(r.get(PRODUCT_REDIS_KEY))[str(category.pk)]
        if len(products) < limit: limit = len(products)
        products_ids = map(lambda x: x[0], sorted(products.items(), key=lambda x: x[1], reverse=True)[:limit])
        return category.products.filter(id__in=products_ids)


def recaptcha_check(request):
    data = {
        'response': request.POST.get('g-recaptcha-response'),
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY
    }
    resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    resp_json = resp.json()
    return True if resp_json['score'] > 0.5 and resp_json['success'] == True else False
