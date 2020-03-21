from django import forms
from .models import Train


class TrainForm(forms.ModelForm):
    name = forms.CharField(label='Поезд', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название поезда'}))
    class Meta:
        model = Train
        fields = ('name', 'from_city', 'to_city', 'travel_time',)
