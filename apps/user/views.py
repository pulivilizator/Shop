import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import views as auth_views, login
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.conf import settings

from . import forms

from apps.shop_app import utils, models

class CastomLoginView(utils.DataMixin, auth_views.LoginView):
    template_name = 'user/login.html'
    success_url = reverse_lazy('shop:home')
    form_class = forms.LoginForm

    def get_success_url(self):
        return reverse_lazy('shop:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        up_context = self.get_user_context(title='Войти в аккаунт')
        context.update(up_context)
        return context


@method_decorator(login_required, name='dispatch')
class CastomLogoutView(utils.DataMixin, auth_views.LogoutView):
    success_url = reverse_lazy('user:login')

    def get_success_url(self):
        return reverse_lazy('user:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        up_context = self.get_user_context(title='Выход')
        context.update(up_context)
        return context

class CastomRegisterView(utils.DataMixin, generic.CreateView):
    template_name = 'user/register.html'
    success_url = reverse_lazy('shop:home')
    form_class = forms.RegisterForm

    def get_success_url(self):
        return reverse_lazy('shop:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        up_context = self.get_user_context(title='Регистрация', recaptcha_site_key=settings.GOOGLE_RECAPTCHA_PUBLIC_KEY)
        context.update(up_context)
        return context
    
    def form_valid(self, form):
        if self.request.POST.get('politics') is None:
            form.error_messages['politics'] = 'Примите согласие на обработку персональных данных'
            return self.form_invalid(form)
        is_bot = utils.recaptcha_check(self.request)
        if is_bot:
            user = form.save()
            login(self.request, user)
            return redirect('shop:home')
        return super().form_valid(form)

class ResetPasswordView(utils.DataMixin, auth_views.PasswordResetView):
    template_name = 'user/reset_passwd.html'
    form_class = forms.ResetPasswordForm
    email_template_name = 'user/email_template_passwd.html'
    success_url = reverse_lazy('user:reset_passwd_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        up_context = self.get_user_context(title='Восстановление пароля')
        context.update(up_context)
        return context

class PasswdResetConfirm(utils.DataMixin, auth_views.PasswordResetConfirmView):
    template_name = 'user/passwd_confirm.html'
    success_url = reverse_lazy('user:login')
    form_class = forms.PasswordConfirmForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        up_context = self.get_user_context(title='Установите новый пароль')
        context.update(up_context)
        return context


class PasswdResetDone(utils.DataMixin, auth_views.PasswordResetDoneView):
    template_name = 'user/passwd_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        up_context = self.get_user_context(title='Письмо успешно отправлено')
        context.update(up_context)
        return context

@method_decorator(login_required, name='dispatch')
class ProfileView(utils.DataMixin, generic.TemplateView):
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        products = models.Product.objects.all()
        up_context = self.get_user_context(title='Личный кабинет', user=user, products=products)
        context.update(up_context)
        return context


def download_file(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'politics/agree.docx')
    if 'politic' in request.GET:
        file_path = os.path.join(settings.MEDIA_ROOT, 'politics/politic.docx')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
