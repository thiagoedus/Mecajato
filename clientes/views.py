import json
import re

from django.core import serializers
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Carro, Cliente


def adiciona_cliente(request):
    if request.method == 'GET':
        return render(request, 'clientes/clientes.html')
    
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


        return redirect('/clientes/atualiza_cliente_id/')
    

def att_cliente_id(request):
    clientes_list = Cliente.objects.all()
    return render(request, 'clientes/atualiza_cliente.html', {'clientes': clientes_list})

def att_cliente(request):
    id_cliente = request.POST.get('id_cliente')
    cliente = Cliente.objects.filter(id=id_cliente)
    cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields']
    cliente_id = json.loads(serializers.serialize('json', cliente))[0]

    carros = Carro.objects.filter(cliente_id=id_cliente)
    carros_json = json.loads(serializers.serialize('json', carros))
    carros_json = [{'fields': carro['fields'], 'id': carro['pk']} for carro in carros_json]
    data = {'cliente': cliente_json, 'carros': carros_json, 'cliente_id': cliente_id}

    return JsonResponse(data)

@csrf_exempt
def update_carro(request, id):
    nome_carro = request.POST.get("carros")
    placa = request.POST.get("placas")
    ano = request.POST.get("anos")

    carro = Carro.objects.get(id=id)
    list_placas = Carro.objects.filter(placa=placa).exclude(id=id)
    if list_placas.exists():
        return {'status': '500'}
    carro.carro = nome_carro
    carro.placa = placa
    carro.ano = ano
    carro.save()    
    

    return redirect('/clientes/atualiza_cliente_id')


def excluir_carro(request, id):
    try:
        carro = Carro.objects.get(id=id)
        carro.delete()
        return redirect(reverse('atualiza_clientes_id')+f'?aba=atualiza_cliente_id&id_cliente={id}')
    except:
        return redirect(reverse('atualiza_clientes_id'))
    
def update_cliente(request, id):
    dados_cliente = Cliente.objects.get(id=id)

    nome = dados_cliente.nome
    sobrenome = dados_cliente.sobrenome
    email = dados_cliente.email
    cpf = dados_cliente.cpf

    list_cpf = Cliente.objects.filter(cpf=cpf).exclude(id=id)
    if list_cpf.exists():
        return JsonResponse({"status":"500"})
    
    list_email = Cliente.objects.filter(email=email).exclude(id=id)
    if list_email.exists():
        return JsonResponse({"status":"500"})

    cliente = get_object_or_404(Cliente, id=id)

    try:
        cliente.nome = nome
        cliente.sobrenome = sobrenome
        cliente.email = email
        cliente.cpf = cpf
        cliente.save()
        return JsonResponse({'status': '200', 'nome': nome, 'sobrenome': sobrenome, 'email': email, 'cpf' : cpf})
    except:
        return JsonResponse({'status': '500'})
