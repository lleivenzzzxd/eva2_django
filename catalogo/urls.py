from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_videojuegos, name='lista_videojuegos'),
    path('juego/<int:pk>/', views.detalle, name='detalle'),
    path('agregar/<int:pk>/', views.agregar, name='agregar'),
    path('quitar/<int:pk>/', views.quitar, name='quitar'),
    path('carrito/', views.carrito, name='carrito'),
    path('checkout/', views.checkout, name='checkout'),
    path('pedido/<int:pk>/', views.pedido_ok, name='pedido_ok'),
]
