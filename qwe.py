import redis
from shop import settings
import json
import pickle

CATEGORY_REDIS_KEY = 'category:views'
PRODUCT_REDIS_KEY = 'product:views'
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB, )
cat_ids = json.loads(r.get(CATEGORY_REDIS_KEY))

print(*map(lambda x: x[0], sorted(cat_ids.items(), key=lambda x: x[1], reverse=True)[:3]))