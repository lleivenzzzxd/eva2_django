from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_videojuegos, name='lista_videojuegos'),
]
