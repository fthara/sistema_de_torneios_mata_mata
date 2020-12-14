from django.test import TestCase

from competidor.forms import CompetidorForm


# Create your tests here.
class CompetidorFormTestCase(TestCase):
    def test_competidor_form_valido(self):
        form = CompetidorForm(
            data={
                "nome_competidor": "Bayern de Munique",
                "pais": "Alemanha",
                "estado": "Munique",
            }
        )
        self.assertTrue(form.is_valid())

    def test_competidor_form_invalido(self):
        form = CompetidorForm(data={})
        self.assertFalse(form.is_valid())
