from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.livros.models import Livro
from apps.livros.forms import ImportarGoogleBooksApiForms, LivroForms
from apps.livros.services.google_books_service import (
    listar_google_books,
    get_livro_google_books_api,
)
from helpers.erros_helper import tratar_erros
from math import ceil

PAGE_SIZE = 10


def index(request, page=1):
    artigo_busca = ""
    if "artigo_busca" in request.GET:
        artigo_busca = request.GET["artigo_busca"]
    start_index = (int(page) - 1) * PAGE_SIZE
    end_index = int(page) * PAGE_SIZE
    livros = Livro.objects.filter(titulo__icontains=artigo_busca).order_by("titulo")[
        start_index:end_index
    ]
    total_items = Livro.objects.filter(titulo__icontains=artigo_busca).count()
    total_pages = ceil(total_items / PAGE_SIZE)
    if page == 1:
        last_page = 1
    else:
        last_page = page - 1
    if page == total_pages:
        next_page = total_pages
    else:
        next_page = page + 1
    return render(
        request,
        "livros/index.html",
        {
            "cards": livros,
            "last_page": last_page,
            "page": page,
            "next_page": next_page,
            "page_size": PAGE_SIZE,
            "total_items": total_items,
            "total_pages": total_pages,
        },
    )


def importar_google_books_api(request):
    if not request.user.is_authenticated:
        messages.warning(
            request, "Você precisa estar logado para utilizar esta ferramenta."
        )
        return redirect("index")

    form = ImportarGoogleBooksApiForms()
    if request.method == "POST":
        form = ImportarGoogleBooksApiForms(request.POST)
        if form.is_valid():
            codigo_barras_isbn = form.cleaned_data["codigo_barras_isbn"]
            titulo = form.cleaned_data["titulo"]
            livros = listar_google_books(codigo_barras_isbn, titulo)
            return render(
                request,
                "livros/importar_google_books_api.html",
                {"form": form, "cards": livros},
            )

    return render(
        request,
        "livros/importar_google_books_api.html",
        {"form": form},
    )


def salvar_livro_google_books_api(request, codigo_barras_isbn: str):
    if not request.user.is_authenticated:
        messages.warning(
            request, "Você precisa estar logado para utilizar esta ferramenta."
        )
        return redirect("index")
    livro_model = Livro.objects.get_or_create(codigo_barras_isbn=codigo_barras_isbn)
    livro_import = get_livro_google_books_api(codigo_barras_isbn)
    livro_model[0].titulo = livro_import.titulo
    livro_model[0].subtitulo = livro_import.subtitulo
    livro_model[0].autores = livro_import.autores
    livro_model[0].data_publicacao = livro_import.data_publicacao
    livro_model[0].descricao = livro_import.descricao
    livro_model[0].url_capa = livro_import.url_capa
    livro_model[0].codigo_barras_isbn = codigo_barras_isbn
    livro_model[0].save()
    return render(request, "livros/livro.html", {"livro": livro_model[0]})


def livro(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    return render(request, "livros/livro.html", {"livro": livro})


def novo_livro(request):
    if not request.user.is_authenticated:
        messages.warning(
            request, "Você precisa estar logado para adicionar um novo livro."
        )
        return redirect("index")

    form = LivroForms

    if request.method == "POST":
        form = LivroForms(request.POST, request.FILES)
        if form.is_valid():
            livro = form.save()
            livro.save()
            messages.success(request, "Livro adicionado com sucesso!")
            return redirect("livro", livro_id=livro.id)
        else:
            tratar_erros(form, request)
    return render(request, "livros/novo_livro.html", {"form": form})


def editar_livro(request, livro_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Você precisa estar logado para editar um livro.")
        return redirect("index")

    livro = get_object_or_404(Livro, pk=livro_id)
    form = LivroForms(instance=livro)

    if request.method == "POST":
        form = LivroForms(request.POST, request.FILES, instance=livro)
        if form.is_valid():
            form.save()
            messages.success(request, "Livro editado com sucesso!")
            return redirect("livro", livro_id=livro_id)
        else:
            tratar_erros(form, request)
    return render(
        request, "livros/editar_livro.html", {"form": form, "livro_id": livro_id}
    )


def excluir_livro(request, livro_id):
    if not request.user.is_authenticated:
        messages.warning(
            request, "Você precisa estar logado para utilizar esta ferramenta."
        )
        return redirect("index")

    livro = get_object_or_404(Livro, pk=livro_id)
    livro.delete()
    messages.success(request, "Livro excluído com sucesso.")

    return redirect("index")
