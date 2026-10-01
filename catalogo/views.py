from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Categoria, Videojuego


def lista_videojuegos(request):
    q = request.GET.get('q', '')
    cat_sel = request.GET.get('cat', '')

    videojuegos = Videojuego.objects.select_related('categoria').order_by('titulo')
    if q:
        videojuegos = videojuegos.filter(titulo__icontains=q)
    if cat_sel:
        videojuegos = videojuegos.filter(categoria_id=cat_sel)

    paginator = Paginator(videojuegos, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'catalogo/lista.html', {
        'page_obj': page_obj,
        'categorias': Categoria.objects.order_by('nombre'),
        'q': q,
        'cat_sel': cat_sel,
        'total': paginator.count,
    })
