from django.contrib import admin
from .models import Train

# Register your models here.

@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('name', 'from_city', 'to_city', 'travel_time',)
