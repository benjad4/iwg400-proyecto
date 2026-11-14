from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import ResenaForm
from .models import Panorama

METODOS_PAGO = {
    'efectivo': 'acepta_efectivo',
    'tarjeta': 'acepta_tarjeta',
    'transferencia': 'acepta_transferencia',
}


def lista_panoramas(request):
    panoramas = Panorama.objects.all()

    comuna = request.GET.get('comuna', '')
    categoria = request.GET.get('categoria', '')
    cocina = request.GET.get('cocina', '')
    costo = request.GET.get('costo', '')
    junaeb = request.GET.get('junaeb', '')
    personas = request.GET.get('personas', '')
    pago = request.GET.get('pago', '')
    accesible = request.GET.get('accesible', '')
    mascotas = request.GET.get('mascotas', '')
    ninos = request.GET.get('ninos', '')

    if comuna:
        panoramas = panoramas.filter(comuna=comuna)
    if categoria:
        panoramas = panoramas.filter(categoria=categoria)
    if cocina:
        panoramas = panoramas.filter(tipo_cocina=cocina)
    if costo == 'gratis':
        panoramas = panoramas.filter(costo=0)
    elif costo == 'pago':
        panoramas = panoramas.filter(costo__gt=0)
    if junaeb:
        panoramas = panoramas.filter(acepta_junaeb=True)
    if personas.isdigit():
        panoramas = panoramas.filter(
            Q(capacidad_maxima__isnull=True) | Q(capacidad_maxima__gte=int(personas))
        )
    if pago in METODOS_PAGO:
        panoramas = panoramas.filter(**{METODOS_PAGO[pago]: True})
    if accesible:
        panoramas = panoramas.filter(accesible=True)
    if mascotas:
        panoramas = panoramas.filter(acepta_mascotas=True)
    if ninos:
        panoramas = panoramas.filter(apto_ninos=True)

    comunas = (Panorama.objects.order_by('comuna')
               .values_list('comuna', flat=True).distinct())
    categorias = (Panorama.objects.order_by('categoria')
                  .values_list('categoria', flat=True).distinct())
    cocinas = (Panorama.objects.exclude(tipo_cocina='')
               .order_by('tipo_cocina')
               .values_list('tipo_cocina', flat=True).distinct())
    datos_mapa = list(panoramas.values('nombre', 'latitud', 'longitud'))

    return render(request, 'panoramas/lista.html', {
        'panoramas': panoramas,
        'datos_mapa': datos_mapa,
        'comunas': comunas,
        'categorias': categorias,
        'cocinas': cocinas,
        'comuna_elegida': comuna,
        'categoria_elegida': categoria,
        'cocina_elegida': cocina,
        'costo_elegido': costo,
        'junaeb': junaeb,
        'personas': personas,
        'pago_elegido': pago,
        'accesible': accesible,
        'mascotas': mascotas,
        'ninos': ninos,
    })


def detalle_panorama(request, pk):
    panorama = get_object_or_404(Panorama, pk=pk)

    if request.method == 'POST':
        form = ResenaForm(request.POST)
        if form.is_valid():
            resena = form.save(commit=False)
            resena.panorama = panorama
            resena.save()
            return redirect('detalle_panorama', pk=pk)
    else:
        form = ResenaForm()

    resenas = panorama.resenas.all()
    promedio = resenas.aggregate(Avg('valoracion'))['valoracion__avg']

    return render(request, 'panoramas/detalle.html', {
        'panorama': panorama,
        'resenas': resenas,
        'promedio': promedio,
        'form': form,
        'esta_guardado': pk in request.session.get('guardados', []),
    })


@require_POST
def guardar_panorama(request, pk):
    get_object_or_404(Panorama, pk=pk)
    guardados = request.session.get('guardados', [])
    if pk not in guardados:
        guardados.append(pk)
    request.session['guardados'] = guardados
    return redirect('detalle_panorama', pk=pk)


@require_POST
def quitar_panorama(request, pk):
    guardados = request.session.get('guardados', [])
    if pk in guardados:
        guardados.remove(pk)
    request.session['guardados'] = guardados
    return redirect('mis_guardados')


def mis_guardados(request):
    ids = request.session.get('guardados', [])
    panoramas = Panorama.objects.filter(pk__in=ids)
    return render(request, 'panoramas/guardados.html', {'panoramas': panoramas})


def elegir_comuna(request):
    comunas = (Panorama.objects.values('comuna')
               .annotate(total=Count('id')).order_by('comuna'))
    return render(request, 'panoramas/comunas.html', {'comunas': comunas})



def elegir_categoria(request):
    comuna = request.GET.get('comuna', '')
    if not comuna:
        return redirect('elegir_comuna')
    categorias = (Panorama.objects.filter(comuna=comuna)
                  .values('categoria').annotate(total=Count('id'))
                  .order_by('categoria'))
    return render(request, 'panoramas/categorias.html', {
        'comuna': comuna,
        'categorias': categorias,
    })