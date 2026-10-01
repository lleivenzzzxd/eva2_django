from catalogo.models import Videojuego

n = 0
for v in Videojuego.objects.filter(imagen=''):
    v.imagen = f"https://picsum.photos/seed/pv{v.pk}/460/215"
    v.save()
    n += 1
print("Fotos asignadas:", n)
