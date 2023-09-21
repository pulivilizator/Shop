from django import template

from ..models import Category

register = template.Library()


@register.inclusion_tag('shop_app/includes/categories.html')
def show_categories():
    categories = Category.objects.filter(category=None).order_by().prefetch_related('subcategories')
    return {'categories': categories}
