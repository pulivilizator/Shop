from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .likes import Likes
from apps.shop_app import utils, models


class LikesView(utils.DataMixin, generic.ListView):
    template_name = 'likes/likes.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        up_context = self.get_user_context(title='Избранное')
        context.update(up_context)

        return context

    def get_queryset(self):
        likes = Likes(self.request)
        prods = models.Product.objects.filter(id__in=likes.likes.keys())
        return prods

def add_to_likes(request, product_id):
    likes = Likes(request)
    product = get_object_or_404(models.Product, id=product_id)
    likes.add(product)
    return JsonResponse({'success': True,})


def remove_from_likes(request, product_id):
    likes = Likes(request)
    product = get_object_or_404(models.Product, id=product_id)
    likes.delete(product)
    return JsonResponse({'success': True,})


def clear_likes(request):
    likes = Likes(request)
    likes.clear()
    print(123123)
    return JsonResponse({'success': True})
