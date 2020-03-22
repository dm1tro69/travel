from django import forms
from .models import Rout
from cities.models import City


class RoutForm(forms.Form):
    from_city = forms.ModelChoiceField(label='Откуда', queryset=City.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control js-example-basic-single'}))
    to_city = forms.ModelChoiceField(label='Куда', queryset=City.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control js-example-basic-single'}))
    across_cities = forms.ModelMultipleChoiceField(label='Через города', required=False, queryset=City.objects.all(),
                                                   widget=forms.SelectMultiple(attrs={'class': 'form-control js-example-basic-multiple'}))

    traveling_time = forms.IntegerField(label='Время в пути', widget=forms.NumberInput(attrs={'class': 'form-control'}))
