from django.contrib import admin
from .models import Categoria, Videojuego

admin.site.register(Categoria)
admin.site.register(Videojuego)
from .models import Pedido, ItemPedido
admin.site.register(Pedido)
admin.site.register(ItemPedido)
