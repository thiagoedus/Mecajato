import json
import re

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Carro, Cliente


def home(request):
    if request.method == 'GET':
        clientes_list = Cliente.objects.all()
        return render(request, 'clientes/clientes.html', {'clientes': clientes_list})
    
    elif request.method == 'POST':
        nome = request.POST.get("nome")
        sobrenome = request.POST.get("sobrenome")
        email = request.POST.get("email")
        cpf = request.POST.get("cpf")
        carros = request.POST.getlist("carros")
        placas = request.POST.getlist("placas")
        anos = request.POST.getlist("anos")

        cliente = Cliente.objects.filter(cpf=cpf)

        if cliente.exists():
            return render(request, 'clientes/clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'email': email, 'carros': zip(carros, placas, anos)})
        
        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'clientes/clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'cpf': cpf, 'carros': zip(carros, placas, anos)})

        cliente=Cliente(
            nome = nome,
            sobrenome = sobrenome,
            email = email,
            cpf = cpf
        )

        cliente.save()

        for car, placa, ano in zip(carros, placas, anos):
            carro = Carro(carro=car, placa=placa, ano=ano, cliente=cliente)
            carro.save()


        return HttpResponse('teste')
    

def att_cliente(request):
    id_cliente = request.POST.get('id_cliente')
    cliente = Cliente.objects.filter(id=id_cliente)
    cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields']

    carros = Carro.objects.filter(cliente_id=id_cliente)
    carros_json = json.loads(serializers.serialize('json', carros))
    carros_json = [{'fields': carro['fields'], 'id': carro['pk']} for carro in carros_json]
    data = {'cliente': cliente_json, 'carros': carros_json}

    return JsonResponse(data)

@csrf_exempt
def update_carro(request, id):
    nome_carro = request.POST.get("carros")
    placa = request.POST.get("placas")
    ano = request.POST.get("anos")

    carro = Carro.objects.get(id=id)
    list_placas = Carro.objects.filter(placa=placa).exclude(id=id)
    if list_placas.exists():
        return HttpResponse("Placa já existe")
    carro.carro = nome_carro
    carro.placa = placa
    carro.ano = ano
    carro.save()    
    

    return HttpResponse('Deu certo')


def excluir_carro(request, id):
    try:
        carro = Carro.objects.get(id=id)
        carro.delete()
        return redirect(reverse('clientes')+f'aba=atualiza_cliente&id_cliente={id}')
    except:
        return redirect(reverse('clientes'))