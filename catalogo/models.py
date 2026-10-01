from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Videojuego(models.Model):
    titulo = models.CharField(max_length=150)
    precio = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.URLField(max_length=400, blank=True, default='')
    descripcion = models.TextField(blank=True, default='')
    desarrollador = models.CharField(max_length=200, blank=True, default='')
    fecha = models.CharField(max_length=50, blank=True, default='')
    capturas = models.TextField(blank=True, default='')
    req_min = models.TextField(blank=True, default='')
    req_rec = models.TextField(blank=True, default='')

    def lista_capturas(self):
        return [c for c in self.capturas.split('\n') if c]

    def __str__(self):
        return self.titulo


class Pedido(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    total = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.pk} - {self.nombre}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=150)
    precio = models.IntegerField()
    cantidad = models.IntegerField()
