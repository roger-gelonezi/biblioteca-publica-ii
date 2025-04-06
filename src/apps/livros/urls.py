from django.urls import path
from apps.livros.views import (
    index,
    livro,
    importar_google_books_api,
    novo_livro,
    editar_livro,
    excluir_livro,
)

urlpatterns = [
    path("", index, name="index"),
    path("<int:page>", index, name="index"),
    path("livro/<int:livro_id>", livro, name="livro"),
    path("novo-livro", novo_livro, name="novo_livro"),
    path("editar-livro/<int:livro_id>", editar_livro, name="editar_livro"),
    path(
        "importar-google-books-api",
        importar_google_books_api,
        name="importar_google_books_api",
    ),
    path("excluir_livro/<int:livro_id>", excluir_livro, name="excluir_livro"),
]
