from copy import deepcopy
from decimal import Decimal as D

from django.conf import settings

from apps.shop_app import models


class Likes:
    def __init__(self, request):
        self.session = request.session
        likes = self.session.get(settings.LIKES_SESSION_ID)
        if not likes:
            likes = self.session[settings.LIKES_SESSION_ID] = {}
        self.likes = likes

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.likes:
            self.likes[product_id] = {'price': str(product.price)}
        self.save()

    def delete(self, product):
        product_id = str(product.id)
        if product_id in self.likes:
            del self.likes[product_id]

        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.likes.keys()
        products = models.Product.objects.filter(id__in=product_ids)
        likes = deepcopy(self.likes)
        for product in products:
            likes[str(product.id)]['product'] = product

        for item in likes.values():
            item['price'] = D(item['price'])
            print(item)
            yield item

    def __len__(self):
        return len(self.likes)

    def clear(self):
        self.likes = self.session[settings.LIKES_SESSION_ID] = {}
        self.save()
