from django.urls import path
from . import views


app_name = 'train'

urlpatterns = [
    path('', views.home, name='home'),
    path('detail/<int:pk>/', views.TrainDetailView.as_view(), name='detail'),
    path('add/', views.TrainCreateView.as_view(), name='add'),
    path('update/<int:pk>/', views.TrainUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.TrainDeleteView.as_view(), name='delete'),
]