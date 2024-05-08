from django import template

from .. import utils
from ..models import Category

register = template.Library()


@register.inclusion_tag('shop_app/includes/categories.html')
def show_categories():
    categories = Category.objects.filter(category=None).order_by().prefetch_related('subcategories')
    return {'categories': categories}


@register.inclusion_tag('shop_app/includes/categories_footer.html')
def show_categories_footer():
    categories = utils.get_populated_cats(7)
    return {'categories': categories}
