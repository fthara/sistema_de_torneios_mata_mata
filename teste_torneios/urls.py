"""teste_torneios URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

from competidor.forms import CompetidorForm
from competidor.views import (
    CompetidorDelete,
    CompetidorUpdate,
    adicionar_competidor,
    competidor_list,
    competidor_view,
)
from comum.views import comum_view
from torneio.forms import AddCompetidorForm, ResultadoForm, TorneioForm
from torneio.views import (
    TorneioDelete,
    TorneioUpdate,
    adicionar_torneio,
    cadastro_resultado,
    inicia_torneio,
    listar_4_primeiros,
    remove_competidor_torneio,
    torneio_list,
    view_rodadas,
    view_torneio,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # user auth urls
    path("", comum_view, name="home"),
    path("torneio/adicionar_torneio", adicionar_torneio, name="adicionar_torneio"),
    path("torneio/buscar_torneio", torneio_list, name="buscar_torneio"),
    path(
        "torneio/editar_torneio/<int:pk>/",
        TorneioUpdate.as_view(),
        name="editar_torneio",
    ),
    path(
        "torneio/deletar_torneio/<int:pk>/",
        TorneioDelete.as_view(),
        name="deletar_torneio",
    ),
    path("torneio/exibir_torneio/<int:pk>/", view_torneio, name="exibir_torneio"),
    path(
        "torneio/<int:pk_torneio>/del_competidor_torneio/<int:pk_comp>/",
        remove_competidor_torneio,
        name="del_competidor_torneio",
    ),
    path("torneio/iniciar_torneio/<int:pk>/", inicia_torneio, name="iniciar_torneio"),
    path(
        "torneio/<int:pk_torneio>/ver_partidas_da_rodada/<int:num_rodada>",
        view_rodadas,
        name="deletar_competidor",
    ),
    path(
        "torneio/<int:pk_torneio>/resultado_partida/<int:pk_partida>/",
        cadastro_resultado,
        name="resultado_partida",
    ),
    path(
        "torneio/<int:pk>/listar_4_primeiros/",
        listar_4_primeiros,
        name="listar_4_primeiros",
    ),
    path(
        "competidor/adicionar_competidor",
        adicionar_competidor,
        name="adicionar_competidor",
    ),
    path("competidor/buscar_competidor", competidor_list, name="buscar_competidor"),
    path(
        "competidor/exibir_competidor/<int:pk>",
        competidor_view,
        name="exibir_competidor",
    ),
    path(
        "competidor/editar_competidor/<int:pk>/",
        CompetidorUpdate.as_view(),
        name="editar_competidor",
    ),
    path(
        "competidor/deletar_competidor/<int:pk>/",
        CompetidorDelete.as_view(),
        name="deletar_competidor",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
