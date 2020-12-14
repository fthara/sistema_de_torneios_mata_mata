from django.contrib import admin

from .models import Partida, Torneio


# Register your models here.
# Registro do bd no admin do django
class TorneioAdmin(admin.ModelAdmin):
    search_fields = ["nome_torneio"]
    list_display = ("nome_torneio", "tipo_torneio", "modalidade")


admin.site.register(Torneio, TorneioAdmin)


class PartidaAdmin(admin.ModelAdmin):
    search_fields = ["id"]
    list_display = ("torneio", "competidor1", "competidor2", "vencedor", "num_rodada")


admin.site.register(Partida, PartidaAdmin)
