from django.contrib import admin
from .models import Panorama


@admin.register(Panorama)
class PanoramaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'comuna', 'costo', 'acepta_junaeb')
    list_filter = ('categoria', 'comuna', 'acepta_junaeb')
    search_fields = ('nombre', 'direccion')