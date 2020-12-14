import django_filters

from .models import Competidor


class CompetidorFilter(django_filters.FilterSet):
    ORDENAR = (("ascending", "Ascendente"), ("descending", "Descendente"))

    ordering = django_filters.ChoiceFilter(
        label="Ordernar", choices=ORDENAR, method="filter_by_order"
    )
    nome_competidor = django_filters.CharFilter(
        label="Nome do Competidor", lookup_expr="icontains"
    )
    pais = django_filters.CharFilter(label="Pais")
    estado = django_filters.CharFilter(label="Estado")

    class Meta:
        model = Competidor
        fields = [
            "nome_competidor",
            "pais",
            "estado",
        ]

    def filter_by_order(self, queryset, name, value):
        expression = "nome_competidor" if value == "ascending" else "-nome_competidor"
        return queryset.order_by(expression)
