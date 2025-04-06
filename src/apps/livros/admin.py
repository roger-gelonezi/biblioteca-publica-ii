from django.contrib import admin

from apps.livros.models import Livro


class ListarLivros(admin.ModelAdmin):
    list_display = ("id", "titulo")
    list_per_page = 20


admin.site.register(Livro, ListarLivros)
