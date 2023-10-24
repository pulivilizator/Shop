from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from . import forms, models, tasks
from apps.shop_app import utils
from apps.cart.cart import Cart


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

