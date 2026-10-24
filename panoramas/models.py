from django.db import models


class Panorama(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=50)
    direccion = models.CharField(max_length=200)
    comuna = models.CharField(max_length=80)
    latitud = models.FloatField()
    longitud = models.FloatField()
    costo = models.PositiveIntegerField(default=0)
    horario = models.CharField(max_length=100, blank=True)
    acepta_junaeb = models.BooleanField(default=False)
    tipo_cocina = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.nombre
