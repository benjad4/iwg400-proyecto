from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.elegir_comuna, name='elegir_comuna'),
    path('categorias/', views.elegir_categoria, name='elegir_categoria'),
    path('mapa/', views.lista_panoramas, name='lista_panoramas'),
    path('panorama/<int:pk>/', views.detalle_panorama, name='detalle_panorama'),
    path('panorama/<int:pk>/guardar/', views.guardar_panorama, name='guardar_panorama'),
    path('panorama/<int:pk>/quitar/', views.quitar_panorama, name='quitar_panorama'),
    path('guardados/', views.mis_guardados, name='mis_guardados'),
    path('sorpresa/', views.sorpresa, name='sorpresa'),
    path('entrar/', auth_views.LoginView.as_view(template_name='panoramas/login.html'), name='login'),
    path('salir/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
]