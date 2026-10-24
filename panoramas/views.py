from django.shortcuts import render
from .models import Panorama


def lista_panoramas(request):
    panoramas = Panorama.objects.all()
    return render(request, 'panoramas/lista.html', {'panoramas': panoramas})