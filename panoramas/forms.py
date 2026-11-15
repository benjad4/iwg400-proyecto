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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['valoracion'].choices = (
            [('', 'Elige una valoración')]
            + [(i, f'{i} de 5') for i in range(1, 6)]
        )