from django.shortcuts import render
from .models import Panorama


def lista_panoramas(request):
    panoramas = Panorama.objects.all()
    datos_mapa = list(panoramas.values('nombre', 'latitud', 'longitud'))
    return render(request, 'panoramas/lista.html', {
        'panoramas': panoramas,
        'datos_mapa': datos_mapa,
    })