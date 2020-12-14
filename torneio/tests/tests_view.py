import json

from django.test import TestCase
from django.urls import reverse

from torneio.models import Torneio

# Create your tests here.

# Teste para adicionar o torneio
class AdicionaTorneioTestCase(TestCase):
    # Verifica de retorna o código html 200
    def test_status_code_200(self):
        response = self.client.get(reverse("adicionar_torneio"))
        self.assertEquals(response.status_code, 200)

    # Verifica de retorna o código html 200 e se os valores estão sendo inseridos no bd
    def test_adicionar_torneio(self):
        url = reverse("adicionar_torneio")
        response = self.client.post(
            url,
            {
                "nome_torneio": "torneio1",
                "tipo_torneio": "Nacional",
                "modalidade": "volei",
            },
        )

        self.assertEquals(response.status_code, 200)
        torneio = Torneio.objects.get(id=1)
        self.assertEquals(torneio.nome_torneio, "torneio1")
        self.assertEquals(torneio.tipo_torneio, "Nacional")
        self.assertEquals(torneio.modalidade, "volei")


# Teste para a página de lista de torneios
class ListaTorneioTestCase(TestCase):
    # Verifica de retorna o código html 200
    def test_torneio_list_GET(self):
        response = self.client.get(reverse("buscar_torneio"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "buscar_torneio.html")


# Teste para deletar o torneio
class DeletaTorneioTestCase(TestCase):
    # Verifica de retorna o código html 302 para depois deletar.
    def test_torneio_delete(self):
        torneio = Torneio.objects.create(
            nome_torneio="torneio1", tipo_torneio="Nacional", modalidade="volei"
        )

        url = reverse("deletar_torneio", kwargs={"pk": torneio.pk})

        response = self.client.delete(url, json.dumps({"id": torneio.pk}))

        torneios = Torneio.objects.all()
        self.assertEquals(response.status_code, 302)
        self.assertEquals(torneios.count(), 0)
