import requests

from apps.livros.models import Livro

__base_url = "https://www.googleapis.com/books/v1/volumes?q="


def __extract_industry_identifiers(livro_google_books: dict) -> str:
    identifiers = livro_google_books.get("industryIdentifiers", [])
    print(identifiers)
    isbn_default: str = ""
    for identifier in identifiers:
        if identifier.get("type") == "ISBN_13":
            return identifier.get("identifier")
        else:
            isbn_default = identifier.get("identifier")
    return isbn_default


def __get_google_book_as_livro(link_google_api: str) -> Livro:
    response = requests.get(link_google_api)
    dados_json = response.json()
    livro_google_books = dados_json.get("volumeInfo", {})
    livro = Livro()
    livro.titulo = livro_google_books.get("title", "")
    livro.subtitulo = livro_google_books.get("subtitle", "")
    livro.autores = livro_google_books.get("authors", [])
    livro.data_publicacao = livro_google_books.get("publishedDate", "")
    livro.descricao = livro_google_books.get("description", "")
    livro.url_capa = livro_google_books.get("imageLinks", {}).get("thumbnail")
    livro.codigo_barras_isbn = __extract_industry_identifiers(livro_google_books)
    return livro


def __validate_response(response: requests.Response) -> bool:
    if response is None:
        return False
    if not isinstance(response, requests.Response):
        return False
    if response.status_code != 200:
        return False
    return True


def __validate_content(dados_json: dict) -> bool:
    if dados_json is None:
        return False
    if not isinstance(dados_json, dict):
        return False
    if "items" not in dados_json:
        return False
    if "totalItems" not in dados_json:
        return False
    if dados_json.get("totalItems", 0) == 0:
        return False
    return True


def __get_from_google_books_api(url: str) -> list[Livro]:
    response = requests.get(url)
    if not __validate_response(response):
        return []

    dados_json = response.json()
    if not __validate_content(dados_json):
        return []

    volumes = dados_json.get("items", [])
    volumes_response: list[Livro] = []
    for volume in volumes:
        self_link = volume.get("selfLink")
        livro = __get_google_book_as_livro(self_link)
        if livro:
            volumes_response.append(livro)
    return volumes_response


def __volumes_por_titulo(titulo: str) -> list[Livro]:
    if not titulo:
        return []
    url = f"{__base_url}intitle:{titulo}"
    return __get_from_google_books_api(url)


def __volumes_por_codigo_barras(codigo_barras_isbn: str) -> list[Livro]:
    if not codigo_barras_isbn:
        return []
    url = f"{__base_url}isbn:{codigo_barras_isbn}"
    return __get_from_google_books_api(url)


def __buscar_volumes(codigo_barras_isbn: str, titulo: str) -> list[Livro]:
    volumes_por_codigo_barras = __volumes_por_codigo_barras(codigo_barras_isbn)
    volumes_por_titulo = __volumes_por_titulo(titulo)
    return volumes_por_codigo_barras + volumes_por_titulo


def listar_google_books(codigo_barras_isbn: str, titulo: str):
    return __buscar_volumes(codigo_barras_isbn, titulo)


def get_livro_google_books_api(codigo_barras_isbn: str) -> Livro:
    livros = __volumes_por_codigo_barras(codigo_barras_isbn)
    if livros and len(livros) > 0:
        livro = livros[0]
        return livro
    return None
