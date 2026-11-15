from django import forms
from .models import Resena


class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['valoracion', 'comentario']
        labels = {
            'valoracion': 'Valoración (1 a 5)',
            'comentario': 'Comentario',
        }