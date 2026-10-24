from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_panoramas, name='lista_panoramas'),
]