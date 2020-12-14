from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.shortcuts import get_object_or_404

from competidor.models import Competidor

from .models import Partida, Torneio

# Escolhas para o tipo de torneio
TIPO_TORNEIO = (
    ("", "Choose..."),
    ("Municipal", "Municipal"),
    ("Estadual", "Estadual"),
    ("Nacional", "Nacional"),
    ("Mundial", "Mundial"),
)

# Formulário que cria os torneios, sem os competidores
class TorneioForm(forms.ModelForm):
    nome_torneio = forms.CharField(label="Nome do Torneio")
    tipo_torneio = forms.ChoiceField(choices=TIPO_TORNEIO)
    modalidade = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Ex: Futebol, volei..."}),
        label="Modalidade",
    )

    class Meta:
        model = Torneio
        fields = [
            "nome_torneio",
            "tipo_torneio",
            "modalidade",
        ]


# Formulário que adiciona os competidores no torneio
class AddCompetidorForm(forms.ModelForm):
    competidor = forms.ModelChoiceField(
        queryset=Competidor.objects.all(), label="Escolha o Competidor"
    )

    class Meta:
        model = Torneio
        fields = [
            "competidor",
        ]

    def save(self):
        instance = super(AddCompetidorForm, self).save(commit=False)
        competidor = self.cleaned_data["competidor"]
        instance.competidor.add(competidor)
        return instance


# Formulário para marcar os resultados das partidas
class ResultadoForm(forms.ModelForm):
    vencedor = forms.ModelChoiceField(queryset=Competidor.objects, label="vencedor")

    class Meta:
        model = Partida
        fields = [
            "vencedor",
        ]

    # Lista com os dois competidores da partida
    def __init__(self, partida, *args, **kwargs):
        super(ResultadoForm, self).__init__(*args, **kwargs)
        self.fields["vencedor"].choices = [
            [None, "Selecione o vencedor"],
            [partida.competidor1.id, partida.competidor1.nome_competidor],
            [partida.competidor2.id, partida.competidor2.nome_competidor],
        ]
        self.instance = partida
