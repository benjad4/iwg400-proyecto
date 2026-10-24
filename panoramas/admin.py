from django.contrib import admin
from .models import Panorama, Resena


@admin.register(Panorama)
class PanoramaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'comuna', 'costo', 'acepta_junaeb')
    list_filter = ('categoria', 'comuna', 'acepta_junaeb')
    search_fields = ('nombre', 'direccion')


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('panorama', 'autor', 'valoracion', 'fecha')
    list_filter = ('valoracion',)