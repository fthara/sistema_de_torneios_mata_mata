import math
import random

from django.db import models
from django.db.models import Max, Q

from competidor.models import Competidor


# Create your models here.
class Torneio(models.Model):
    nome_torneio = models.CharField(max_length=120)
    tipo_torneio = models.CharField(max_length=50)
    modalidade = models.CharField(max_length=120)
    competidor = models.ManyToManyField(Competidor)
    em_andamento = models.BooleanField(default=False)

    # Inicia o torneio. Após isso o botão desaparece para o usuário.
    def iniciar_torneio(self):
        self.em_andamento = True
        self.save()

    # Filtra a ultima rodada do torneio de acordo com as partidas criadas.
    def get_ultima_rodada(self):
        return (
            self.partida_set.all().aggregate(Max("num_rodada")).get("num_rodada__max")
        )

    # Filtra a ultima rodada do torneio de acordo com as partidas criadas.
    def get_total_competidores(self):
        return self.competidor.all().count()

    # Só deixa iniciar o torneio se existe mais de 1 jogador.
    def pode_iniciar_torneio(self):
        return self.get_total_competidores() > 1 and not self.em_andamento

    # Verifica se a rodada está encerrada. Se não existe partida sem vencedores naquela rodada, ela está enerrada.
    def rodada_esta_encerrada(self, num_rodada):
        return not self.partida_set.filter(
            num_rodada=num_rodada, vencedor=None
        ).exists()

    # Filtra o as partidas pelo numero da rodada
    def get_partidas(self, num_rodada):
        return self.partida_set.filter(num_rodada=num_rodada)

    # Retorna um zip com as rodadas em uma lista
    def get_lista_rodadas(self, acrescenta_um=False):
        ultima_rodada = self.get_ultima_rodada()
        if acrescenta_um:
            ultima_rodada = ultima_rodada + 1

        rodadas = None
        if ultima_rodada != None:
            rodadas = zip(list(range(1, ultima_rodada + 1)))
        return rodadas

    # Retorna o total de rodadas
    def get_total_rodadas(self):
        total_competidores = self.get_total_competidores()
        total_rodadas = 0
        if total_competidores != 0:
            # Calcula o total de rodadas. Log na base 2 do numero total de competidores.
            total_rodadas = math.log(total_competidores, 2)
            if not total_rodadas.is_integer():
                total_rodadas = int(total_rodadas) + 1
        return total_rodadas

    # Retorna as partidas da disputa do 1º e 2º lugar e do 3º e 4º lugar
    def get_finalistas(self):
        # Filtrando a ultima rodada (MAX)
        ultima_rodada = self.get_ultima_rodada()

        # Calculando o total de rodadas
        total_rodadas = self.get_total_rodadas()

        disputa1e2 = None
        disputa3e4 = None

        # Se o torneio está na ultima fase disputa1e2 e disputa3e4 é calculado aqui.
        if ultima_rodada == total_rodadas:
            # Seleciona todas as partidas e filtra pela ultima rodada
            partidas = self.partida_set.all()
            final = partidas.filter(num_rodada=ultima_rodada)
            # Caso o torneio tenha mais de 2 times filtra os 2 ultimos finalistas.
            if total_rodadas > 1:
                # Seleciona as partidas da semifinal
                semifinal = partidas.filter(num_rodada=ultima_rodada - 1)
                # Filtra os id`s dos vencedores
                final1e2 = semifinal.values_list("vencedor__id", flat=True)
                # filtra a a partida do 1º e 2º colocado
                disputa1e2 = final.filter(
                    Q(competidor1=final1e2[0]) | Q(competidor2=final1e2[0])
                ).first()
                # filtra a a partida do 3º e 4º colocado
                disputa3e4 = final.filter(
                    ~Q(competidor1=final1e2[0]), ~Q(competidor2=final1e2[0])
                ).first()
            # Se o torneio tenha apenas 2 times
            else:
                # filtra apenas o unico jogo da final
                disputa1e2 = final.first()

        return disputa1e2, disputa3e4

    # Gera partidas de forma aleatória.
    def gerar_partidas(self, lista_competidores, num_rodada):
        # Sorteia competidores que jogarão entre si
        for i in range(int(len(lista_competidores) / 2)):
            # Escolhe aleatoriamente um jogador
            competidor1_id = random.choice(lista_competidores)
            # Exclui o escolhido da lista de competidores
            lista_competidores.remove(competidor1_id)
            # Escolhe aleatoriamente um jogador
            competidor2_id = random.choice(lista_competidores)
            # Exclui o escolhido da lista de competidores
            lista_competidores.remove(competidor2_id)
            # Cria a partida com os jogadores escolhidos
            Partida(
                torneio=self,
                competidor1=self.competidor.get(pk=competidor1_id),
                competidor2=self.competidor.get(pk=competidor2_id),
                num_rodada=num_rodada,
            ).save()


class Partida(models.Model):
    torneio = models.ForeignKey(
        Torneio,
        related_name="partida_set",
        verbose_name="Torneio",
        on_delete=models.CASCADE,
    )
    competidor1 = models.ForeignKey(
        Competidor,
        related_name="Partida_competidor1",
        verbose_name="Competidor1",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    competidor2 = models.ForeignKey(
        Competidor,
        related_name="Partida_competidor2",
        verbose_name="Competidor2",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    vencedor = models.ForeignKey(
        Competidor,
        related_name="Partida_vencedor",
        verbose_name="Vencedor",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    num_rodada = models.IntegerField(
        verbose_name="Numero da Rodada", null=True, blank=True
    )
