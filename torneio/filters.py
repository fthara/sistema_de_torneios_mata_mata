import django_filters

from competidor.models import Competidor

from .models import Torneio


# Filtragem da lista de torneios
class TorneioFilter(django_filters.FilterSet):
    ORDENAR = (("ascending", "Ascendente"), ("descending", "Descendente"))

    TIPO_TORNEIO = (
        ("Municipal", "Municipal"),
        ("Estadual", "Estadual"),
        ("Nacional", "Nacional"),
        ("Mundial", "Mundial"),
    )

    ordering = django_filters.ChoiceFilter(
        label="Ordernar", choices=ORDENAR, method="filter_by_order"
    )
    nome_torneio = django_filters.CharFilter(
        label="Nome do Torneio", lookup_expr="icontains"
    )
    tipo_torneio = django_filters.ChoiceFilter(label="Tipo", choices=TIPO_TORNEIO)
    modalidade = django_filters.CharFilter(label="Modalidade")
    competidor = django_filters.ModelChoiceFilter(
        label="Competidor", queryset=Competidor.objects.all()
    )

    class Meta:
        model = Torneio
        fields = [
            "nome_torneio",
            "tipo_torneio",
            "modalidade",
            "competidor",
        ]

    def filter_by_order(self, queryset, name, value):
        expression = "nome_torneio" if value == "ascending" else "-nome_torneio"
        return queryset.order_by(expression)
