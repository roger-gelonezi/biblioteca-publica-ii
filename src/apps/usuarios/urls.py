from django.urls import path

from apps.usuarios.views import entrar, novo_usuario, sair

urlpatterns = [
    path("entrar", entrar, name="entrar"),
    path("novo-usuario", novo_usuario, name="novo_usuario"),
    path("sair", sair, name="sair"),
]
