from django.db.models import (
    CharField,
    Model,
    TextField,
)
from django_mysql.models import ListTextField


class Livro(Model):
    titulo = CharField(max_length=100)
    subtitulo = CharField(max_length=100, null=True, blank=True)
    descricao = TextField(null=True, blank=True)
    autores = ListTextField(base_field=CharField(max_length=50), null=True, blank=True)
    data_publicacao = CharField(max_length=10, null=True, blank=True)
    url_capa = CharField(max_length=500, null=True, blank=True)
    codigo_barras_isbn = CharField(max_length=30, null=True, blank=True)
