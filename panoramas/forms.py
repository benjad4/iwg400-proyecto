from django import forms
from .models import Resena


class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['autor', 'valoracion', 'comentario']
        labels = {
            'autor': 'Tu nombre',
            'valoracion': 'Valoración (1 a 5)',
            'comentario': 'Comentario',
        }