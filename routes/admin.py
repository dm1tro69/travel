from django.contrib import admin
from .models import Rout

# Register your models here.

@admin.register(Rout)
class RoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'from_city', 'to_city', 'travel_times',)
