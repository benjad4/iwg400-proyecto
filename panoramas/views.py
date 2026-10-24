from django.shortcuts import get_object_or_404, render
from .models import Panorama


def lista_panoramas(request):
    panoramas = Panorama.objects.all()

    comuna = request.GET.get('comuna', '')
    costo_max = request.GET.get('costo_max', '')
    junaeb = request.GET.get('junaeb', '')

    if comuna:
        panoramas = panoramas.filter(comuna=comuna)
    if costo_max.isdigit():
        panoramas = panoramas.filter(costo__lte=int(costo_max))
    if junaeb:
        panoramas = panoramas.filter(acepta_junaeb=True)

    comunas = (Panorama.objects.order_by('comuna')
               .values_list('comuna', flat=True).distinct())
    datos_mapa = list(panoramas.values('nombre', 'latitud', 'longitud'))

    return render(request, 'panoramas/lista.html', {
        'panoramas': panoramas,
        'datos_mapa': datos_mapa,
        'comunas': comunas,
        'comuna_elegida': comuna,
        'costo_max': costo_max,
        'junaeb': junaeb,
    })


def detalle_panorama(request, pk):
    panorama = get_object_or_404(Panorama, pk=pk)
    return render(request, 'panoramas/detalle.html', {'panorama': panorama})