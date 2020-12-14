from django.test import TestCase

from competidor.models import Competidor


# Create your tests here.
class CompetidorTestCase(TestCase):
    def setUp(self):
        Competidor.objects.create(
            nome_competidor="Bayern de Munique", pais="Alemanha", estado="Munique"
        )

    def test_retorno_str(self):
        c1 = Competidor.objects.get(nome_competidor="Bayern de Munique")
        self.assertEquals(c1.__str__(), "Bayern de Munique")
