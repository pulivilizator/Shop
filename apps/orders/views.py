from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic

from . import forms, models, tasks
from apps.shop_app import utils
from apps.cart.cart import Cart

import weasyprint


class CreateOrderView(utils.DataMixin, generic.CreateView):
    form_class = forms.OrderCreateForm
    template_name = 'orders/create_order.html'
    success_url = reverse_lazy('payment:process')

    def get_success_url(self):
        return reverse_lazy('payment:process')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        up_context = self.get_user_context(title='Оформление заказа', user=self.request.user)
        context.update(up_context)
        return context

    def form_valid(self, form):
        cart = Cart(self.request)
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        super().form_valid(form)
        for item in cart:
            models.OrderItem.objects.create(order=self.object,
                                            product=item['product'],
                                            quantity=item['quantity'],
                                            price=item['price'])
        tasks.order_created.delay(self.object.id)
        self.request.session['order_id'] = self.object.id
        cart.clear()
        return redirect('payment:process')


class DetailOrderView(utils.DataMixin, generic.DetailView):
    model = models.Order
    pk_url_kwarg = 'order_id'
    slug_url_kwarg = 'username'
    template_name = 'orders/detail_order.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_staff or self.request.user.username == self.kwargs['username']:
            context = super().get_context_data(**kwargs)
            up_context = self.get_user_context(title=f'Заказ №{self.kwargs["order_id"]}',
                                               buy=False, order_id=self.kwargs["order_id"],
                                               products=self.object.items.all().select_related('product'),
                                               total_price=self.object.get_total_price)

            context.update(up_context)
            return context

        raise Http404

@staff_member_required
def order_pdf(request, order_id):
    order = get_object_or_404(models.Order, pk=order_id)
    html = render_to_string('orders/pdf.html', {'order': order})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order_id}.pdf'

    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(
                                               settings.STATIC_ROOT / 'css/pdf.css'
                                           )])
    return response