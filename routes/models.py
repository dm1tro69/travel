from django.db import models
#from cities.models import City
from trains.models import Train

# Create your models here.

class Rout(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название маршрута', unique=True)
    from_city = models.CharField(max_length=100, verbose_name='Откуда')
    to_city = models.CharField(max_length=100, verbose_name='Куда')
    across_cities = models.ManyToManyField(Train, blank=True, verbose_name='Через города')
    travel_times = models.IntegerField(verbose_name='Время в пути')

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        ordering = ['name']
