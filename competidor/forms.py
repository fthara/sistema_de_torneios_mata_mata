from django import forms

from .models import Competidor


class CompetidorForm(forms.ModelForm):
    nome_competidor = forms.CharField(label="Nome do Competidor")
    pais = forms.CharField(label="País de Origem")
    estado = forms.CharField(label="Estado de Origem")

    class Meta:
        model = Competidor
        fields = [
            "nome_competidor",
            "pais",
            "estado",
        ]
