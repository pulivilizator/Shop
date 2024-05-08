from django import forms
from django.contrib.auth import forms as auth_forms, password_validation
from django.contrib.auth.models import User


class LoginForm(auth_forms.AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'placeholder': 'Введите Ваш логин или E-mail'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Введите Ваш пароль'}))

class RegisterForm(auth_forms.UserCreationForm):
    username = auth_forms.UsernameField(label='username', widget=forms.TextInput(attrs={'placeholder': 'Укажите ваш никнейм'}))
    email = forms.EmailField(label='email', widget=forms.TextInput(attrs={'placeholder': 'Укажите Ваш E-Mail'}))
    password1 = forms.CharField(label='password1', widget=forms.PasswordInput(attrs={'placeholder': 'Укажите Ваш пароль'}))
    password2 = forms.CharField(label='password1', widget=forms.PasswordInput(attrs={'placeholder': 'Повторите Ваш пароль'}))


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email уже используется')
        return data

class ResetPasswordForm(auth_forms.PasswordResetForm):
    email = forms.EmailField(label='email', max_length=254,
                             widget=forms.EmailInput(attrs={'placeholder': 'Ведите Ваш E-mail'}))


class PasswordConfirmForm(auth_forms.SetPasswordForm):
    new_password1 = forms.CharField(
        label=("Новый пароль"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                   'placeholder': 'Введите новый пароль'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label=("Повторите пароль"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'placeholder': 'Повторите пароль'}),
    )

