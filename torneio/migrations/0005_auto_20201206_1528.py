# Generated by Django 3.1.4 on 2020-12-06 15:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("competidor", "0003_remove_competidor_torneios"),
        ("torneio", "0004_partida"),
    ]

    operations = [
        migrations.AlterField(
            model_name="partida",
            name="competidor1",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="Partida_competidor1",
                to="competidor.competidor",
                verbose_name="Competidor1",
            ),
        ),
        migrations.AlterField(
            model_name="partida",
            name="competidor2",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="Partida_competidor2",
                to="competidor.competidor",
                verbose_name="Competidor2",
            ),
        ),
    ]
