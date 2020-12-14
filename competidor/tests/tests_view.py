import json

from django.test import TestCase
from django.urls import reverse

from competidor.models import Competidor


# Create your tests here.
class AdicionaCompetidorTestCase(TestCase):
    # Verifica de retorna o código html 200
    def test_status_code_200(self):
        response = self.client.get(reverse("adicionar_competidor"))
        self.assertEquals(response.status_code, 200)

    # Verifica de retorna o código html 200 e se os valores estão sendo inseridos no bd
    def test_adicionar_competidor(self):
        url = reverse("adicionar_competidor")
        response = self.client.post(
            url, {"nome_competidor": "Comp1", "pais": "pais1", "estado": "estado1"}
        )

        self.assertEquals(response.status_code, 200)
        competidor = Competidor.objects.get(id=1)
        self.assertEquals(competidor.nome_competidor, "Comp1")
        self.assertEquals(competidor.pais, "pais1")
        self.assertEquals(competidor.estado, "estado1")

    # Verifica se retorna 0 quando não tem competidores cadastrados
    def test_competidor_vazio(self):
        url = reverse("adicionar_competidor")
        self.competidor = Competidor.objects.all()

        response = self.client.post(url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.competidor.count(), 0)

    # Verifica se chama o tempalte corretamente
    def test_template_adicionar_competidor(self):
        response = self.client.get(reverse("adicionar_competidor"))
        self.assertTemplateUsed(response, "adicionar_competidor.html")


class ListaCompetidorTestCase(TestCase):
    # Verifica se retorna o template correto
    def test_competidor_list_GET(self):
        response = self.client.get(reverse("buscar_competidor"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "buscar_competidor.html")


class DeletaCompetidorTestCase(TestCase):
    # Verifica se a função delete retorna o número 302
    def test_competidor_delete(self):
        competidor = Competidor.objects.create(
            nome_competidor="Comp1", pais="pais1", estado="estado1"
        )

        url = reverse("deletar_competidor", kwargs={"pk": competidor.pk})

        response = self.client.delete(url, json.dumps({"id": competidor.pk}))

        competidores = Competidor.objects.all()
        self.assertEquals(response.status_code, 302)
        self.assertEquals(competidores.count(), 0)
