from django.shortcuts import render
from django.http import HttpResponse
from .models import Cliente, Carro
import re

def home(request):
    if request.method == 'GET':
        return render(request, 'clientes/clientes.html')
    elif request.method == 'POST':
        name = request.POST.get("nome")
        sobrenome = request.POST.get("sobrenome")
        email = request.POST.get("email")
        cpf = request.POST.get("cpf")
        carros = request.POST.getlist("carros")
        placas = request.POST.getlist("placas")
        anos = request.POST.getlist("anos")

        cliente = Cliente.objects.filter(cpf=cpf)

        if cliente.exists():
            return render(request, 'clientes/clientes.html', {'nome': name, 'sobrenome': sobrenome, 'email': email, 'carros': zip(carros, placas, anos)})
        
        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'clientes/clientes.html', {'nome': name, 'sobrenome': sobrenome, 'cpf': cpf, 'carros': zip(carros, placas, anos)})

        cliente=Cliente(
            nome = name,
            sobrenome = sobrenome,
            email = email,
            cpf = cpf
        )

        cliente.save()

        for car, placa, ano in zip(carros, placas, anos):
            carro = Carro(carro=car, placa=placa, ano=ano, cliente=cliente)
            carro.save()


        return HttpResponse('teste')