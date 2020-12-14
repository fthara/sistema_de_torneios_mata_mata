from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, UpdateView

from .filters import CompetidorFilter
from .forms import CompetidorForm
from .models import Competidor


# Create your views here.
# Cria novos competidores
def adicionar_competidor(request):
    form = CompetidorForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = CompetidorForm()

    context = {"form": form}
    return render(request, "adicionar_competidor.html", context)


def competidor_view(request, pk):
    competidor = get_object_or_404(Competidor, pk=pk)
    context = {}
    context["competidor"] = competidor
    template_name = "exibir_competidor.html"

    return render(request, template_name, context)


# Atualiza dados dos competidores
class CompetidorUpdate(UpdateView):
    form_class = CompetidorForm
    model = Competidor
    template_name = "editar_competidor.html"
    success_url = reverse_lazy("buscar_competidor")


# Deleta competidor
class CompetidorDelete(DeleteView):
    model = Competidor
    template_name = "competidor_confirm_delete.html"
    success_url = reverse_lazy("buscar_competidor")


# Visualiza os competidores com o filtro
def competidor_list(request):
    context = {}
    template_name = "buscar_competidor.html"
    # Filtro dos comepetidores
    filtered_competidores = CompetidorFilter(
        request.GET, queryset=Competidor.objects.all()
    )

    context["filtered_competidores"] = filtered_competidores
    # Define quantos competidores serão exibidos na página
    paginated_filtered_competidores = Paginator(filtered_competidores.qs, 5)
    page_number = request.GET.get("page")
    competidor_page_obj = paginated_filtered_competidores.get_page(page_number)

    try:
        items = paginated_filtered_competidores.page(page_number)
    except PageNotAnInteger:
        items = paginated_filtered_competidores.page(1)
    except EmptyPage:
        items = paginated_filtered_competidores.page(
            paginated_filtered_competidores.num_pages
        )
    # Calcula o numero de páginas que serão exibidos na paginação.
    index = competidor_page_obj.number - 1
    max_index = len(paginated_filtered_competidores.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginated_filtered_competidores.page_range[start_index:end_index]

    context["competidor_page_obj"] = competidor_page_obj
    context["page_range"] = page_range
    context["items"] = items

    return render(request, template_name, context)
