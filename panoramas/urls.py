from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_panoramas, name='lista_panoramas'),
    path('panorama/<int:pk>/', views.detalle_panorama, name='detalle_panorama'),
    path('panorama/<int:pk>/guardar/', views.guardar_panorama, name='guardar_panorama'),
    path('panorama/<int:pk>/quitar/', views.quitar_panorama, name='quitar_panorama'),
    path('guardados/', views.mis_guardados, name='mis_guardados'),
]