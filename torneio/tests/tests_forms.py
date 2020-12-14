from django.test import TestCase

from competidor.models import Competidor
from torneio.forms import AddCompetidorForm, ResultadoForm, TorneioForm
from torneio.models import Partida, Torneio


# Testes para o formulário de adicionar torneios
class TorneioFormTestCase(TestCase):
    # Verifica se o form criado é valido
    def test_torneio_form_valido(self):
        form = TorneioForm(
            data={
                "nome_torneio": "Torneio 1",
                "tipo_torneio": "Nacional",
                "modalidade": "Futebol",
            }
        )
        self.assertTrue(form.is_valid())

    # Verifica se o form vazio retorna false
    def test_torneio_form_invalido(self):
        form = TorneioForm(data={})
        self.assertFalse(form.is_valid())

    # Verifica se o tipo de torneio, que é do tipo ChoiceField, retorna inválido quando não está nas opções
    def test_torneio_form_tipo_torneio_invalido(self):
        form = TorneioForm(
            data={
                "nome_torneio": "Torneio 1",
                "tipo_torneio": "Gelatina",
                "modalidade": "Futebol",
            }
        )
        self.assertFalse(form.is_valid())


# Testes para o formulário que adiciona o competidor no torneio.
class AddCompetidorFormTestCase(TestCase):
    # Criação de competidores
    def setUp(self):
        self.comp1 = Competidor.objects.create(
            nome_competidor="Comp1", pais="pais1", estado="estado1"
        )

    # Verifica se a adição de competidores é válida
    def test_adiciona_competidor_form_valido(self):
        form_data = {"competidor": self.comp1.pk}
        form = AddCompetidorForm(form_data)
        self.assertTrue(form.is_valid())


# Testes para o formulário de adicionar resultados das partidas
class ResultadoFormTestCase(TestCase):
    # Cria competidores, torneio e partida
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

        self.partida = Partida.objects.create(
            torneio=self.torneio,
            competidor1=self.comp1,
            competidor2=self.comp2,
            num_rodada=1,
        )

    # Verifica se o form criado é válido.
    def test_resultado_form_valido(self):
        p1 = Partida.objects.get(pk=self.partida.pk)
        vencedor = p1.competidor1.id
        form_data = {"vencedor": vencedor}

        form = ResultadoForm(p1, form_data)
        self.assertTrue(form.is_valid())
