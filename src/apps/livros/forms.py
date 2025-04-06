from django import forms
from apps.livros.models import Livro


class ImportarGoogleBooksApiForms(forms.Form):
    codigo_barras_isbn = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Código de Barras (ISBN)",
    )
    titulo = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Título",
        required=False,
    )


class LivroForms(forms.ModelForm):
    class Meta:
        model = Livro
        fields = [
            "titulo",
            "subtitulo",
            "autores",
            "data_publicacao",
            "url_capa",
            "codigo_barras_isbn",
            "descricao",
        ]
        labels = {
            "titulo": "Título",
            "subtitulo": "Subtítulo",
            "descricao": "Descrição",
            "autores": "Autores e Tradutores (separados por vírgula)",
            "data_publicacao": "Data de publicação",
            "url_capa": "URL da Capa do livro",
            "codigo_barras_isbn": "Código de Barras (ISBN)",
        }
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "subtitulo": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(
                attrs={"class": "form-control", "style": "height: 200px;"}
            ),
            "autores": forms.TextInput(attrs={"class": "form-control"}),
            "data_publicacao": forms.TextInput(attrs={"class": "form-control"}),
            "url_capa": forms.TextInput(attrs={"class": "form-control"}),
            "codigo_barras_isbn": forms.TextInput(attrs={"class": "form-control"}),
        }
