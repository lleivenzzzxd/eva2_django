from catalogo.models import Videojuego

BASE = "https://cdn.akamai.steamstatic.com/steam/apps/{}/header.jpg"
ids = {
    "Elden Ring": 1245620, "The Witcher 3": 292030, "Cyberpunk 2077": 1091500,
    "Baldur's Gate 3": 1086940, "Grand Theft Auto V": 271590,
    "Stardew Valley": 413150, "Terraria": 105600, "Hollow Knight": 367520,
    "Celeste": 504230, "Portal 2": 620, "Among Us": 945360,
    "Undertale": 391540, "Valheim": 892970, "Counter-Strike 2": 730,
    "Apex Legends": 1172470, "Hades": 1145360, "Cuphead": 268910,
    "Red Dead Redemption 2": 1174180, "Project Zomboid": 108600,
}

n = 0
for titulo, appid in ids.items():
    n += Videojuego.objects.filter(titulo=titulo).update(imagen=BASE.format(appid))

for v in Videojuego.objects.filter(descripcion=''):
    v.descripcion = (f"{v.titulo} es un videojuego de la categoría {v.categoria}. "
                     "Clave digital de entrega inmediata, lista para activar en tu cuenta.")
    v.save()

print("Juegos con foto real:", n)
