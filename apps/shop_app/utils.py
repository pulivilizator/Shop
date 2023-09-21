

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        auth = self.request.user.is_authenticated
        context['auth'] = auth
        return context

def get_hit_products(category):
    return category.products.filter(hit=True)