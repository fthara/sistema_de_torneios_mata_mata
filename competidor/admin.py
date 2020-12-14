from django.contrib import admin

from .models import Competidor


# Register your models here.
class CompetidorAdmin(admin.ModelAdmin):
    search_fields = ["nome_competidor"]
    list_display = ("nome_competidor", "pais", "estado")


admin.site.register(Competidor, CompetidorAdmin)
