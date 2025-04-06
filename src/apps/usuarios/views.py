from django.shortcuts import render, redirect
from apps.usuarios.forms import EntrarForms, NovoUsuarioForms
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from helpers.erros_helper import tratar_erros


def entrar(request):
    form = EntrarForms()

    if request.method == "POST":
        form = EntrarForms(request.POST)
        if form.is_valid():
            user_email = form["email_usuario"].value()
            senha = form["senha"].value()

            user = User.objects.filter(email=user_email).first()
            if user:
                usuario = auth.authenticate(
                    request, username=user.username, password=senha
                )
                if usuario:
                    auth.login(request, usuario)
                    messages.success(request, "Login efetuado com sucesso")
                    return redirect("index")

            messages.warning(request, "Dados de login incorretos")
            return redirect("entrar")

    return render(request, "usuarios/entrar.html", {"form": form})


def novo_usuario(request):
    form = NovoUsuarioForms()

    if request.method == "POST":
        form = NovoUsuarioForms(request.POST)
        if form.is_valid():
            nome = form["nome_cadastro"].value().title()
            email = form["email"].value()
            senha = form["senha_1"].value()

            if User.objects.filter(username=nome).exists():
                messages.warning(request, "Usuário já cadastrado no sistema")
                return redirect("novo_usuario")

            if User.objects.filter(email=email).exists():
                messages.warning(request, "E-mail já cadastrado no sistema")
                return redirect("novo_usuario")

            usuario = User.objects.create_user(
                username=nome, email=email, password=senha, is_active=False
            )
            usuario.save()
            messages.success(
                request,
                "Seu cadastro foi enviado para aprovação, você receberá um e-mail quando aprovado",
            )
            auth.login(request, usuario)
            return redirect("index")
        else:
            tratar_erros(form, request)

    return render(request, "usuarios/novo_usuario.html", {"form": form})


def sair(request):
    auth.logout(request)
    messages.success(request, "Você saiu do sistema com sucesso.")
    return redirect("index")
