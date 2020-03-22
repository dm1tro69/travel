from django.urls import path
from . import views

app_name = 'rout'

urlpatterns = [
    path('', views.home, name='home'),
    path('find/', views.find_routes, name='find'),
]