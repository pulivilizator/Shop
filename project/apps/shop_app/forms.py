from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control search-input',
               'placeholder': 'search...',
               'id': 'search_input'}))
