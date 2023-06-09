from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Servico

from .forms import FormServico


def novo_servico(request):
    if request.method == 'GET':
        form = FormServico
        return render(request, 'servicos/novo_servico.html', context={"form":form})

    elif request.method == 'POST':
        form = FormServico(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse("Salvo com sucesso")
        else:
            return render(request, 'novo_servico.html', {'form': form})
        

def listar_servico(request):
    if request.method == 'GET':
        servicos = Servico.objects.all()
        return render(request, 'servicos/listar_servico.html', {"servicos": servicos})
    
def servico(request, identificador):
    servico = get_object_or_404(Servico, identificador=identificador)
    return render(request, 'servicos/servico.html', {"servico": servico})