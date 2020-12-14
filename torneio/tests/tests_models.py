import math
import random

from django.db.models import Max, Q
from django.test import TestCase

from competidor.models import Competidor
from torneio.models import Partida, Torneio


# Create your tests here.
class TorneioTestCase(TestCase):
    # Cria competidores, torneio e partidas
    def setUp(self):
        self.comp1 = Competidor.objects.create(
            nome_competidor="Comp1", pais="pais1", estado="estado1"
        )

        self.comp2 = Competidor.objects.create(
            nome_competidor="Comp2", pais="pais2", estado="estado2"
        )

        self.comp3 = Competidor.objects.create(
            nome_competidor="Comp3", pais="pais3", estado="estado3"
        )

        self.torneio = Torneio.objects.create(
            nome_torneio="torneio1",
            tipo_torneio="Nacional",
            modalidade="Futebol",
            em_andamento=False,
        )

        self.partida1 = Partida.objects.create(
            torneio=self.torneio,
            competidor1=self.comp1,
            competidor2=self.comp2,
            num_rodada=1,
        )

        self.partida2 = Partida.objects.create(
            torneio=self.torneio,
            competidor1=self.comp1,
            competidor2=self.comp2,
            num_rodada=2,
        )

    # Filtra a ultima rodada do torneio de acordo com as partidas criadas.
    def test_get_ultima_rodada(self):
        t1 = Torneio.objects.get(nome_torneio="torneio1")
        partidas = t1.partida_set.all()
        ultima_rodada = partidas.aggregate(Max("num_rodada")).get("num_rodada__max")
        self.assertEquals(2, ultima_rodada)

    # Filtra a ultima rodada do torneio de acordo com as partidas criadas.
    def test_get_total_competidores(self):
        t1 = Torneio.objects.get(nome_torneio="torneio1")
        contar_antes = t1.competidor.count()
        t1.competidor.add(self.comp1)
        t1.competidor.add(self.comp2)
        contar_depois = t1.competidor.count()
        self.assertNotEquals(contar_antes, contar_depois)

    # Retorna uma lista de rodadas contadas 1 até a ultima rodada gerada para o torneio
    def test_get_lista_rodadas(self):
        t1 = Torneio.objects.get(nome_torneio="torneio1")
        ultima_rodada = (
            t1.partida_set.all().aggregate(Max("num_rodada")).get("num_rodada__max")
        )
        acrescenta_um = False
        if acrescenta_um:
            ultima_rodada = ultima_rodada + 1
        rodadas = None
        if ultima_rodada != None:
            rodadas = list(range(1, 2 + 1))
            rodadas_test = list(range(1, ultima_rodada + 1))

        self.assertEquals(rodadas, rodadas_test)

    # Retorna o total de rodadas
    def test_get_total_rodadas(self):
        t1 = Torneio.objects.get(nome_torneio="torneio1")
        t1.competidor.add(self.comp1, self.comp2, self.comp3)
        total_competidores = t1.competidor.all().count()
        total_rodadas = 0

        if total_competidores != 0:
            # Calcula o total de rodadas. Log na base 2 do numero total de competidores.
            total_rodadas = math.log(total_competidores, 2)
            if not total_rodadas.is_integer():
                total_rodadas = int(total_rodadas) + 1

        self.assertEquals(2, total_rodadas)

    # Gera partidas de forma aleatória.
    def test_gerar_partidas(self):
        lista_competidores = ["comp1", "comp2", "comp3", "comp4"]
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

        self.assertEquals(lista_competidores, [])


class PartidaTestCase(TestCase):
    # Cria competidores, torneio e partida
    def setUp(self):
        self.comp1 = Competidor.objects.create(
            nome_competidor="Comp1", pais="pais1", estado="estado1"
        )

        self.comp2 = Competidor.objects.create(
            nome_competidor="Comp2", pais="pais2", estado="estado2"
        )

        self.torneio = Torneio.objects.create(
            nome_torneio="torneio1",
            tipo_torneio="Nacional",
            modalidade="Futebol",
            em_andamento=False,
        )

        Partida.objects.create(
            torneio=self.torneio,
            competidor1=self.comp1,
            competidor2=self.comp2,
            num_rodada=1,
        )

    # Verifica se existe alguma partida sem vencedor
    def test_partida_vencedor_nulo(self):
        p1 = Partida.objects.get(pk=1)
        self.assertEquals(p1.vencedor, None)

    # Verifica se o competidor 1 é o vencedor da partida
    def test_partida_vencedor_comp1(self):
        p1 = Partida.objects.get(pk=1)
        p1.vencedor = self.comp1
        self.assertEquals(p1.vencedor, self.comp1)

    # Verifica se o competidor 2 é o vencedor da partida
    def test_partida_vencedor_comp2(self):
        p1 = Partida.objects.get(pk=1)
        p1.vencedor = self.comp2
        self.assertEquals(p1.vencedor, self.comp2)
