import random
from catalogo.models import Categoria, Videojuego

random.seed(42)

categorias = [
    "Acción", "RPG", "Deportes", "Aventura", "Terror", "Estrategia",
    "Carreras", "Plataformas", "Shooter", "Simulación", "Mundo Abierto",
    "Indie", "Peleas", "Puzzle", "Supervivencia", "Cooperativo",
]

reales = {
    "Acción": ["God of War Ragnarök", "Devil May Cry 5", "Doom Eternal",
               "Marvel's Spider-Man", "Ghost of Tsushima", "Sekiro", "Hades"],
    "RPG": ["The Witcher 3", "Elden Ring", "Baldur's Gate 3", "Skyrim",
            "Cyberpunk 2077", "Final Fantasy VII Remake", "Persona 5 Royal"],
    "Deportes": ["FIFA 24", "NBA 2K24", "Rocket League", "Gran Turismo 7", "UFC 5"],
    "Aventura": ["Uncharted 4", "Tomb Raider", "Horizon Zero Dawn",
                 "Red Dead Redemption 2", "The Last of Us Part I"],
    "Terror": ["Resident Evil 4", "Silent Hill 2", "Dead Space",
               "Alien: Isolation", "Outlast"],
    "Estrategia": ["Civilization VI", "Age of Empires IV", "XCOM 2",
                   "Total War: Warhammer III", "StarCraft II"],
    "Carreras": ["Forza Horizon 5", "Mario Kart 8 Deluxe", "F1 23",
                 "Need for Speed Heat", "Assetto Corsa"],
    "Plataformas": ["Super Mario Odyssey", "Hollow Knight", "Celeste",
                    "Cuphead", "Sonic Mania"],
    "Shooter": ["Halo Infinite", "Counter-Strike 2", "Apex Legends",
                "Overwatch 2", "Titanfall 2"],
    "Simulación": ["The Sims 4", "Cities: Skylines", "Stardew Valley",
                   "Euro Truck Simulator 2", "Planet Zoo"],
    "Mundo Abierto": ["Grand Theft Auto V", "Minecraft", "Far Cry 6",
                      "No Man's Sky", "Starfield"],
    "Indie": ["Undertale", "Terraria", "Among Us", "Dead Cells", "Disco Elysium"],
    "Peleas": ["Super Smash Bros. Ultimate", "Tekken 8", "Street Fighter 6",
               "Mortal Kombat 1", "Guilty Gear Strive"],
    "Puzzle": ["Portal 2", "Tetris Effect", "The Witness", "Baba Is You"],
    "Supervivencia": ["The Forest", "Valheim", "Rust", "Raft", "Project Zomboid"],
    "Cooperativo": ["It Takes Two", "Deep Rock Galactic", "Helldivers 2",
                    "Overcooked! 2", "Lethal Company"],
}

prefijos = ["Legado", "Sombras", "Furia", "Reino", "Héroes", "Último", "Código",
            "Leyenda", "Cazadores", "Imperio", "Eclipse", "Rebelión", "Destino",
            "Horizonte", "Titanes", "Crónicas", "Guardianes", "Venganza",
            "Odisea", "Despertar"]
sufijos = ["del Dragón", "de Acero", "Perdido", "Infinito", "Oscuro",
           "de las Estrellas", "del Abismo", "Eterno", "de Fuego", "del Norte",
           "Final", "Salvaje", "de Cristal", "Olvidado", "del Caos", "Dorado",
           "de Neón", "Prohibido", "Antiguo", "de la Aurora"]
extras = ["II", "III", "Remastered", "Deluxe", "Redux", "Origins", "Reborn",
          "Definitive Edition", "Legacy", "Zero"]
precios = [0, 4990, 7990, 9990, 12990, 14990, 19990, 24990, 29990,
           34990, 39990, 49990]

META = 40

for nombre_cat in categorias:
    cat, _ = Categoria.objects.get_or_create(nombre=nombre_cat)
    for t in reales.get(nombre_cat, []):
        Videojuego.objects.get_or_create(
            titulo=t,
            defaults={"precio": random.choice(precios), "categoria": cat},
        )
    faltan = META - Videojuego.objects.filter(categoria=cat).count()
    while faltan > 0:
        t = f"{random.choice(prefijos)} {random.choice(sufijos)}"
        if random.random() < 0.6:
            t += " " + random.choice(extras)
        if Videojuego.objects.filter(titulo=t).exists():
            continue
        Videojuego.objects.create(
            titulo=t, precio=random.choice(precios), categoria=cat
        )
        faltan -= 1

print("Categorías:", Categoria.objects.count())
print("Videojuegos:", Videojuego.objects.count())
