from django.contrib import messages


def tratar_erros(form, request):
    for field in form:
        for error in field.errors:
            messages.warning(request, error)
