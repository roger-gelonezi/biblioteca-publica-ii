import requests
from apps.livros.models import Livro


def __buscar_por_isbn(codigo_barras_isbn: str):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{codigo_barras_isbn}"
    response = requests.get(url)
    if response.status_code == 200:
        dados_json = response.json()
        totalItens = dados_json.get("totalItems", 0)
        if totalItens == 0:
            return None
        volume = dados_json.get("items", [])[0]

        self_link = volume.get("selfLink")
        response = requests.get(self_link)
        dados_json = response.json()

        volumeInfo = dados_json.get("volumeInfo", {})
        volumeInfo["id"] = volume.get("id")
        return volumeInfo


def __salvar_livro(codigo_barras_isbn: str, livro):
    livro_model = Livro.objects.get_or_create(codigo_barras_isbn=codigo_barras_isbn)
    livro_model[0].titulo = livro.get("title", "")
    livro_model[0].subtitulo = livro.get("subtitle", "")
    livro_model[0].autores = livro.get("authors", [])
    livro_model[0].data_publicacao = livro.get("publishedDate", "")
    livro_model[0].descricao = livro.get("description", "")
    livro_model[0].url_capa = livro.get("imageLinks", {}).get("thumbnail")
    livro_model[0].codigo_barras_isbn = codigo_barras_isbn
    livro_model[0].save()


def importar_google_books(codigo_barras_isbn: str):
    livro = __buscar_por_isbn(codigo_barras_isbn)
    if livro:
        __salvar_livro(codigo_barras_isbn, livro)
