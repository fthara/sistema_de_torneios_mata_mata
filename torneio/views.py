import math
import random

from django.core.exceptions import PermissionDenied
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import (
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from competidor.models import Competidor

from .filters import TorneioFilter
from .forms import AddCompetidorForm, ResultadoForm, TorneioForm
from .models import Partida, Torneio

# Create your views here.

# Cria novos torneios
def adicionar_torneio(request):
    form = TorneioForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = TorneioForm()

    context = {"form": form}
    return render(request, "adicionar_torneio.html", context)


# Atualiza dados dos torneios
class TorneioUpdate(UpdateView):
    form_class = TorneioForm
    model = Torneio
    template_name = "editar_torneio.html"
    success_url = reverse_lazy("buscar_torneio")


# Deleta torneios
class TorneioDelete(DeleteView):
    model = Torneio
    template_name = "torneio_confirm_delete.html"
    success_url = reverse_lazy("buscar_torneio")


# Lista de todos os torneios com o filtro
def torneio_list(request):
    context = {}
    template_name = "buscar_torneio.html"
    # Filtra os torneios de acordo com o filtro escolhido
    filtered_torneios = TorneioFilter(request.GET, queryset=Torneio.objects.all())
    context["filtered_torneios"] = filtered_torneios
    # Define quantos torneios serão exibidos na página
    paginated_filtered_torneios = Paginator(filtered_torneios.qs, 5)
    page_number = request.GET.get("page")
    torneio_page_obj = paginated_filtered_torneios.get_page(page_number)

    try:
        items = paginated_filtered_torneios.page(page_number)
    except PageNotAnInteger:
        items = paginated_filtered_torneios.page(1)
    except EmptyPage:
        items = paginated_filtered_torneios.page(paginated_filtered_torneios.num_pages)
    # Calcula o numero de páginas que serão exibidos na paginação.
    index = torneio_page_obj.number - 1
    max_index = len(paginated_filtered_torneios.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginated_filtered_torneios.page_range[start_index:end_index]

    context["torneio_page_obj"] = torneio_page_obj
    context["page_range"] = page_range
    context["items"] = items

    return render(request, template_name, context)


# Visualiza os dados do torneio e inclui novos competidores ao torneio.
def view_torneio(request, pk):
    context = {}
    # Chama o torneio de acordo com o seu id
    torneio = get_object_or_404(Torneio, pk=pk)
    context["torneio"] = torneio
    context["competidores"] = torneio.competidor.all()
    # Chama o form que adiciona o competidor. Após o início do torneio esse forms some.
    form = AddCompetidorForm(request.POST or None, instance=torneio)
    if form.is_valid():
        form.save()
        form = AddCompetidorForm()

    (
        context["disputa1e2"],
        context["disputa3e4"],
    ) = torneio.get_finalistas()  # Função do models
    context["form"] = form

    return render(request, "exibir_torneio.html", context)


# Remove o competidor do torneio. Essa função é válida até o início do torneio, após isso o botão some.
def remove_competidor_torneio(request, pk_torneio, pk_comp):
    # Chama o torneio de acordo com o seu id
    torneio = get_object_or_404(Torneio, pk=pk_torneio)
    # Chama o competidor de acordo com o seu id
    competidor_torneio_obj = get_object_or_404(Competidor, pk=pk_comp)
    torneio.competidor.remove(competidor_torneio_obj)

    return redirect("/torneio/exibir_torneio/{}".format(pk_torneio))


# Inicia o torneio e sorteia os jogos da primeira fase.
def inicia_torneio(request, pk):
    # Chama o torneio de acordo com o seu id
    torneio = get_object_or_404(Torneio, pk=pk)

    # Se o torneio inicia com menos de um competidor ele não deixa.
    if not torneio.pode_iniciar_torneio():
        raise PermissionDenied()

    # Chama o total de rodadas e calcula o numero de competidores que irão para o próxima fase
    total_rodadas = torneio.get_total_rodadas()  # Função do models
    num_comp_prox_fase_direto = (
        2 ** total_rodadas
    ) - torneio.get_total_competidores()  # Função do models
    lista_competidores = list(torneio.competidor.values_list("id", flat=True))

    # Caso o torneio tenha mais de uma rodada
    if int(total_rodadas) > 1:
        # Sorteia competidores que vão direto para a próxima fase
        for i in range(0, int(num_comp_prox_fase_direto)):
            competidor_id = random.choice(lista_competidores)
            Partida(
                torneio=torneio,
                competidor1=torneio.competidor.get(pk=competidor_id),
                vencedor=torneio.competidor.get(pk=competidor_id),
                num_rodada=1,
            ).save()
            lista_competidores.remove(competidor_id)

        # Sorteia competidores que jogarão entre si
        torneio.gerar_partidas(lista_competidores, 1)  # Função do models

    # Caso o torneio tenha apenas uma rodada (2 competidores), cria apenas a partida da final.
    else:
        competidor1_id = lista_competidores[0]
        competidor2_id = lista_competidores[1]
        Partida(
            torneio=torneio,
            competidor1=torneio.competidor.get(pk=competidor1_id),
            competidor2=torneio.competidor.get(pk=competidor2_id),
            num_rodada=1,
        ).save()

    # Chama a função para iniciar o torneio.
    torneio.iniciar_torneio()  # Função do models

    return redirect("/torneio/exibir_torneio/{}".format(pk))


# Visualiza as fases do torneio e também cria as partidas após terminada a fase.
def view_rodadas(request, pk_torneio, num_rodada):
    context = {}
    # Chama o torneio de acordo com o seu id
    torneio = get_object_or_404(Torneio, pk=pk_torneio)
    context["torneio"] = torneio
    partidas = torneio.partida_set.all()
    context["partidas"] = partidas.filter(num_rodada=num_rodada)

    # Filtrando a ultima rodada criada no torneio até o momento
    ultima_rodada = torneio.get_ultima_rodada()  # Função do models
    context["rodadas"] = torneio.get_lista_rodadas()  # Função do models
    context["rodada_atual"] = num_rodada
    context["total_rodadas"] = torneio.get_total_rodadas()  # Função do models

    # Calculando o total de rodadas
    total_rodadas = torneio.get_total_rodadas()  # Função do models

    # Caso o torneio tenha mais de uma rodada (mais de 2 times)
    if total_rodadas > 1:
        if ultima_rodada != total_rodadas:
            # Se não existe partida sem vencedor gera próxima fase
            if torneio.rodada_esta_encerrada(ultima_rodada):
                # Atualiza a ultima rodada
                ultima_rodada = ultima_rodada + 1
                rodadas = torneio.get_lista_rodadas(acrescenta_um=True)
                context["rodadas"] = rodadas
                # Se não for o jogo final
                if ultima_rodada != total_rodadas:
                    # Seleciona os vencedores e sorteia os jogos
                    vencedores = torneio.get_partidas(ultima_rodada - 1)
                    lista_competidores = list(
                        vencedores.values_list("vencedor__id", flat=True)
                    )
                    torneio.gerar_partidas(lista_competidores, ultima_rodada)
                # Se o jogo for da final
                else:
                    # Seleciona todos as partidas da seminal
                    partidas = Partida.objects.filter(
                        torneio=pk_torneio, num_rodada=ultima_rodada - 1
                    )
                    # Cria uma lista com os 2 vencedores da semifinal
                    lista_1e2_colocados = list(
                        partidas.values_list("vencedor__id", flat=True)
                    )
                    # Lista todos os competidores da semifinal
                    lista_competidores = list(
                        partidas.values_list("competidor1__id", flat=True)
                    ) + list(partidas.values_list("competidor2__id", flat=True))
                    # Subtrai a lista de competidores com a lista dos vencedores
                    lista_3e4_colocados = list(
                        set(lista_competidores) - set(lista_1e2_colocados)
                    )
                    # Cria as partidas da final (1º e 2º lugar; 3º e 4º lugar)
                    Partida(
                        torneio=torneio,
                        competidor1=torneio.competidor.get(pk=lista_1e2_colocados[0]),
                        competidor2=torneio.competidor.get(pk=lista_1e2_colocados[1]),
                        num_rodada=ultima_rodada,
                    ).save()
                    Partida(
                        torneio=torneio,
                        competidor1=torneio.competidor.get(pk=lista_3e4_colocados[0]),
                        competidor2=torneio.competidor.get(pk=lista_3e4_colocados[1]),
                        num_rodada=ultima_rodada,
                    ).save()
        # Se não estiver na final os valores são None
        context["disputa1e2"], context["disputa3e4"] = torneio.get_finalistas()
    # Caso o torneio tenha apenas 2 times
    else:
        # filtra apenas a partida da disputa do 1º e 2º lugar
        if torneio.rodada_esta_encerrada(ultima_rodada):
            disputa1e2 = partidas.filter(num_rodada=total_rodadas)
            context["disputa1e2"] = disputa1e2
            context["disputa3e4"] = None
        else:
            context["disputa1e2"] = None
            context["disputa3e4"] = None

    return render(request, "partidas.html", context)


# Cadastra os resultados das partidas
def cadastro_resultado(request, pk_partida, pk_torneio):
    context = {}
    # Chama a partida pelo id
    partida = get_object_or_404(Partida, pk=pk_partida)
    # Chama o torneio pelo id
    torneio = get_object_or_404(Torneio, pk=pk_torneio)
    context["partida"] = partida
    context["torneio"] = torneio
    # Filtra o número da rodada da partida.
    num_rodada = partida.num_rodada
    # Pega o resultado do formulário e grava na partida selecionada
    form = ResultadoForm(partida, request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(
            "/torneio/{}/ver_partidas_da_rodada/{}".format(pk_torneio, num_rodada)
        )
    context["form"] = form

    return render(request, "resultado_partida.html", context)


# Lista os priemiros colocados
def listar_4_primeiros(request, pk):
    context = {}
    torneio = get_object_or_404(Torneio, pk=pk)
    context["torneio"] = torneio

    # Filtrando a ultima rodada (MAX)
    total_rodadas = torneio.get_ultima_rodada()
    context["rodadas"] = torneio.get_lista_rodadas()
    # Seleciona o total de partidas e filtra pelo total de rodadas
    partidas = torneio.partida_set.all()
    context["partidas"] = partidas.filter(num_rodada=total_rodadas)

    context["disputa1e2"], context["disputa3e4"] = torneio.get_finalistas()

    return render(request, "listar_4_primeiros.html", context)
