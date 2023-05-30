from django.shortcuts import render


def servicos(request):
    return render(request, 'servicos/novo_servico.html')

def novo_servico(request):
    ...