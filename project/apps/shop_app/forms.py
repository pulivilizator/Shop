from django import forms
from django.urls import reverse


class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control search-input',
               'placeholder': 'search...',
               'id': 'search_input',
               'hx-trigger': 'keyup changed delay:500ms',
               'hx-target': '.options',
               'hx-vars':"{'search_query': document.querySelector('#search_input').value}",
               'hx-swap': 'innerGTML',
               }))

    def __init__(self, *args, **kwargs):
        shop_home_url = kwargs.pop('shop_home_url',
                                   None)  # Получаем URL для 'shop:home'
        super(SearchForm, self).__init__(*args, **kwargs)
        if shop_home_url:
            self.fields['search'].widget.attrs['hx-get'] = shop_home_url
