from django.db import models


# Create your models here.
class Competidor(models.Model):
    nome_competidor = models.CharField(max_length=120)
    pais = models.CharField(max_length=120)
    estado = models.CharField(max_length=120)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.nome_competidor
