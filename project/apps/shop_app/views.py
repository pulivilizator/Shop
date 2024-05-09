from decimal import Decimal as D

from django.contrib.postgres.search import TrigramSimilarity, \
    TrigramWordSimilarity
from django.db.models import Q
from django.views import generic

from . import models
from . import utils
from .forms import SearchForm
from .recommender import Recommender


class HomePage(utils.DataMixin, generic.ListView):
    """Главная страница"""
    template_name = 'shop_app/homepage.html'
    context_object_name = 'elements'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        populated_categories = utils.get_populated_cats(limit=10)
        up_context = self.get_user_context(title='Главная страница',
                                           populated_categories=populated_categories)
        context.update(up_context)
        return context

    def get_queryset(self):
        categories = utils.get_populated_cats()
        return {cat: utils.get_populated_products(cat) for cat in categories}


class CategoryPage(utils.DataMixin, generic.ListView):
    """Список подкатегорий конкретной категории"""
    model = models.Category
    template_name = 'shop_app/category.html'
    context_object_name = 'subcategories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        up_context = self.get_user_context(title=self.category.name,
                                           slug=self.kwargs['category_slug'])
        context.update(up_context)
        return context

    def get_queryset(self):
        self.category = models.Category.objects.get(
            slug=self.kwargs['category_slug'])
        return self.category.subcategories.all()


class SubcategoryPage(utils.DataMixin, generic.ListView):
    """Список товаров подкатегории"""
    model = models.Category
    template_name = 'shop_app/subcategory.html'
    context_object_name = 'products'
    sort = {'price': 'по возрастанию цены',
            '-price': 'по убыванию цены'}
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        properties = self.get_properties(self.object_list)
        up_context = self.get_user_context(title=self.subcategory.name,
                                           slug=self.kwargs['category_slug'],
                                           properties=properties,
                                           checkboxes=self.values,
                                           min_price=self.min_price,
                                           max_price=self.max_price,
                                           sort=self.sort,
                                           sorted_field=self.sorted_field,
                                           select_op=self.sort[
                                               self.sorted_field])
        utils.redis_views_categories(self.subcategory.pk)
        context.update(up_context)
        return context

    def get_queryset(self):
        self.subcategory = models.Category.objects.get(
            slug=self.kwargs['category_slug'])

        self.query_products = self.subcategory.products.all()
        self.min_price = D(self.request.GET.get('min_price').replace(',', '.')) \
            if self.request.GET.get('min_price') \
            else self.query_products.order_by('price')[:1][0].price

        self.max_price = D(self.request.GET.get('max_price').replace(',', '.')) \
            if self.request.GET.get('max_price') \
            else self.query_products.order_by('-price')[:1][0].price

        self.values = dict(self.request.GET)['check'] if self.request.GET.get(
            'check') else []
        self.sorted_field = self.request.GET.get(
            'sort') if self.request.GET.get('sort') else 'price'
        if self.values:
            return set(self.query_products.filter(
                Q(price__gte=self.min_price) &
                Q(price__lte=self.max_price) &
                Q(available=True) &
                Q(properties__value__value__in=self.values)).order_by(
                self.sorted_field))
        else:
            return (
                self.query_products.filter(Q(price__gte=self.min_price) &
                                           Q(price__lte=self.max_price) &
                                           Q(available=True)).order_by(
                    self.sorted_field))

    def get_properties(self, queryset):
        return {p_type: set(p_val for p_val in
                            models.PropertyValue.objects.filter(
                                Q(properties__type=p_type) & Q(
                                    properties__product__in=self.query_products.all())))
                for p_type in
                models.PropertyType.objects.filter(subcategory_field=True)}


class SearchResultsPage(utils.DataMixin, generic.ListView):
    template_name = 'shop_app/subcategory.html'
    context_object_name = 'products'
    sort = {'price': 'по возрастанию цены',
            '-price': 'по убыванию цены'}
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        properties = self.get_properties(self.object_list)
        up_context = self.get_user_context(title=self.search_query_data,
                                           properties=properties,
                                           checkboxes=self.values,
                                           min_price=self.min_price,
                                           search_form=SearchForm(
                                               self.request.GET),
                                           max_price=self.max_price,
                                           sort=self.sort,
                                           sorted_field=self.sorted_field,
                                           select_op=self.sort[
                                               self.sorted_field])
        context.update(up_context)
        return context

    def get_queryset(self):
        self.search_query_data = self.request.GET.get('search')

        self.query_products = models.Product.objects.annotate(
            similarity=(1 / (1 + .4) * TrigramSimilarity('name',
                                                         self.search_query_data) +
                        .4 / (1 + .4) * TrigramWordSimilarity(
                        self.search_query_data, 'description'))
        ).filter(similarity__gt=0.1).order_by('-similarity')

        self.min_price = D(self.request.GET.get('min_price').replace(',', '.')) \
            if self.request.GET.get('min_price') \
            else self.query_products.order_by('price')[:1][0].price

        self.max_price = D(self.request.GET.get('max_price').replace(',', '.')) \
            if self.request.GET.get('max_price') \
            else self.query_products.order_by('-price')[:1][0].price

        self.values = dict(self.request.GET)['check'] if self.request.GET.get(
            'check') else []

        self.sorted_field = self.request.GET.get(
            'sort') if self.request.GET.get('sort') else 'price'

        if self.values:
            return set(self.query_products.filter(
                Q(price__gte=self.min_price) &
                Q(price__lte=self.max_price) &
                Q(available=True) &
                Q(properties__value__value__in=self.values)).order_by(
                self.sorted_field))
        else:
            return set(
                self.query_products.filter(Q(price__gte=self.min_price) &
                                           Q(price__lte=self.max_price) &
                                           Q(available=True)).order_by(
                    self.sorted_field))

    def get_properties(self, queryset):
        return {p_type: set(p_val for p_val in
                            models.PropertyValue.objects.filter(
                                Q(properties__type=p_type) & Q(
                                    properties__product__in=self.query_products.all())))
                for p_type in
                models.PropertyType.objects.filter(subcategory_field=True)}


class ProductPage(utils.DataMixin, generic.DetailView):
    """Страница товара"""
    template_name = 'shop_app/product.html'
    model = models.Product
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, **kwargs):
        utils.redis_views_products(category_id=self.object.subcategory.pk,
                                   element_id=self.object.pk)
        context = super().get_context_data(**kwargs)
        cat = models.Category.objects.filter(
            slug=self.object.subcategory.slug).select_related('category')[0]
        properties = self.get_properties(category=cat, product=self.object)
        r = Recommender()
        recommended_products = r.suggest_products_for([self.object])
        populated_products = utils.get_populated_products(cat, limit=6)
        up_context = self.get_user_context(title=self.object.name,
                                           product=self.object,
                                           subcat=cat, properties=properties,
                                           recommended_products=recommended_products,
                                           populated_products=populated_products)
        context.update(up_context)
        return context

    def get_properties(self, category, product):
        return {group: {prop.type: prop.value
                        for prop in models.Property.objects.filter(
                Q(product=product) & Q(group=group))}
                for group in
                models.PropertyGroup.objects.filter(Q(category=category) &
                                                    Q(properties__in=models.Property.objects.filter(
                                                        product=product)))}
