from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ResenaForm
from .models import Panorama


def lista_panoramas(request):
    panoramas = Panorama.objects.all()

    comuna = request.GET.get('comuna', '')
    categoria = request.GET.get('categoria', '')
    cocina = request.GET.get('cocina', '')
    costo_max = request.GET.get('costo_max', '')
    junaeb = request.GET.get('junaeb', '')

    if comuna:
        panoramas = panoramas.filter(comuna=comuna)
    if categoria:
        panoramas = panoramas.filter(categoria=categoria)
    if cocina:
        panoramas = panoramas.filter(tipo_cocina=cocina)
    if costo_max.isdigit():
        panoramas = panoramas.filter(costo__lte=int(costo_max))
    if junaeb:
        panoramas = panoramas.filter(acepta_junaeb=True)

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
        'costo_max': costo_max,
        'junaeb': junaeb,
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
    })