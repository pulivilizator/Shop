from django import forms

from . import models
from . import widgets


class OrderCreateForm(forms.ModelForm):
    user = forms.HiddenInput()
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите фамилию'}))
    patronymic = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите отчество'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Введите E-mail'}))
    region = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите регион'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите город'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите адрес'}))
    postal_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите индекс'}))

    delivery_method = forms.ModelChoiceField(queryset=models.DeliveryMethod.objects.filter(active=True),
                                             widget=widgets.DeliveryMethodWidget)
    payment_method = forms.ModelChoiceField(queryset=models.PaymentMethod.objects.filter(active=True),
                                            widget=forms.RadioSelect)
    country = forms.ModelChoiceField(queryset=models.Country.objects.filter(active=True),
                                     widget=forms.Select)#, empty_label=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].initial = 1

    class Meta:
        model = models.Order
        fields = ('user', 'first_name', 'last_name', 'patronymic', 'email', 'country', 'region', 'city', 'address', 'postal_code', 'delivery_method', 'payment_method')
