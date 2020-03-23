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


class RoutModelForm(forms.ModelForm):
    name = forms.CharField(label='Название маршрута', widget=forms.TextInput(attrs={'class': 'form-control'}))
    from_city = forms.CharField(widget=forms.HiddenInput())
    to_city = forms.CharField(widget=forms.HiddenInput())
    across_cities = forms.CharField(widget=forms.HiddenInput())
    travel_times = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Rout
        fields = ('name', 'from_city', 'to_city', 'across_cities', 'travel_times',)

