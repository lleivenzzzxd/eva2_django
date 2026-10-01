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


from django.shortcuts import redirect, get_object_or_404
from .models import Pedido, ItemPedido


def _items(request):
    carrito = request.session.get('carrito', {})
    items, total = [], 0
    for j in Videojuego.objects.filter(pk__in=carrito.keys()):
        cant = carrito[str(j.pk)]
        sub = j.precio * cant
        total += sub
        items.append({'juego': j, 'cantidad': cant, 'subtotal': sub})
    return items, total


def agregar(request, pk):
    c = request.session.get('carrito', {})
    c[str(pk)] = c.get(str(pk), 0) + 1
    request.session['carrito'] = c
    return redirect('carrito')


def quitar(request, pk):
    c = request.session.get('carrito', {})
    c.pop(str(pk), None)
    request.session['carrito'] = c
    return redirect('carrito')


def carrito(request):
    items, total = _items(request)
    return render(request, 'catalogo/carrito.html', {'items': items, 'total': total})


def checkout(request):
    items, total = _items(request)
    if not items:
        return redirect('carrito')
    if request.method == 'POST':
        pedido = Pedido.objects.create(
            nombre=request.POST['nombre'], email=request.POST['email'], total=total)
        for i in items:
            ItemPedido.objects.create(
                pedido=pedido, titulo=i['juego'].titulo,
                precio=i['juego'].precio, cantidad=i['cantidad'])
        request.session['carrito'] = {}
        return redirect('pedido_ok', pk=pedido.pk)
    return render(request, 'catalogo/checkout.html', {'items': items, 'total': total})


def pedido_ok(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    return render(request, 'catalogo/pedido_ok.html', {'pedido': pedido})


def detalle(request, pk):
    v = get_object_or_404(Videojuego, pk=pk)
    relacionados = Videojuego.objects.filter(categoria=v.categoria).exclude(pk=pk)[:4]
    return render(request, 'catalogo/detalle.html', {'v': v, 'relacionados': relacionados})
