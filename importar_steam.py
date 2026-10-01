import json, re, time, urllib.request
from catalogo.models import Categoria, Videojuego

def limpiar(s):
    return re.sub('[\U00010000-\U0010FFFF]', '', s or '')

Videojuego.objects.all().delete()
Categoria.objects.all().delete()

ids = list(dict.fromkeys(int(x) for x in open('ids.txt').read().split()))
ok = 0
for appid in ids:
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=cl&l=spanish"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = json.loads(urllib.request.urlopen(req, timeout=20).read())[str(appid)]
    except Exception as e:
        print('Error', appid, e)
        time.sleep(4)
        continue
    if not data.get('success'):
        print('Sin datos', appid)
        continue
    d = data['data']
    if d.get('type') != 'game':
        continue
    if d.get('is_free'):
        precio = 0
    else:
        po = d.get('price_overview')
        if not po:
            print('Sin precio', appid)
            continue
        precio = int(re.sub(r'\D', '', po.get('final_formatted', '')) or 0)
    genres = d.get('genres') or [{'description': 'Otros'}]
    cat, _ = Categoria.objects.get_or_create(nombre=limpiar(genres[0]['description'])[:100])
    pc = d.get('pc_requirements')
    if not isinstance(pc, dict):
        pc = {}
    caps = '\n'.join(s['path_thumbnail'] for s in (d.get('screenshots') or [])[:4])
    try:
        Videojuego.objects.create(
            titulo=limpiar(d['name']).replace('™', '').replace('®', '')[:150],
            precio=precio,
            categoria=cat,
            imagen=d.get('header_image', ''),
            descripcion=limpiar(d.get('short_description', '')),
            desarrollador=limpiar(', '.join(d.get('developers') or []))[:200],
            fecha=(d.get('release_date') or {}).get('date', ''),
            capturas=caps,
            req_min=limpiar(pc.get('minimum', '')),
            req_rec=limpiar(pc.get('recommended', '')),
        )
        ok += 1
        print(ok, d['name'])
    except Exception as e:
        print('No se pudo guardar', appid, e)
    time.sleep(1.6)

print('LISTO. Juegos:', Videojuego.objects.count(), 'Categorías:', Categoria.objects.count())
