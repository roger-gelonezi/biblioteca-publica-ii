from django import forms
from django.core.exceptions import ValidationError


class EntrarForms(forms.Form):
    email_usuario = forms.CharField(
        label="E-mail de cadastro",
        required=True,
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex.: contato@imobiliariaweb.com.br",
            }
        ),
    )
    senha = forms.CharField(
        label="Senha",
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite sua senha",
            }
        ),
    )


class NovoUsuarioForms(forms.Form):
    nome_cadastro = forms.CharField(
        label="Nome de Cadastro e Exibição",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex.: Imobiliária Web",
            }
        ),
    )
    email = forms.EmailField(
        label="E-mail",
        required=True,
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex.: contato@imobiliariaweb.com.br",
            }
        ),
    )
    senha_1 = forms.CharField(
        label="Senha",
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite a sua senha",
            }
        ),
    )
    senha_2 = forms.CharField(
        label="Confirme a sua senha",
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirme a sua senha",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        senha_1 = cleaned_data.get("senha_1")
        senha_2 = cleaned_data.get("senha_2")
        if senha_1 and senha_2 and senha_1 != senha_2:
            self.add_error(
                "senha_2", ValidationError("As senhas digitadas precisam ser iguais")
            )
