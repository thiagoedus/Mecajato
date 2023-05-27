function add_carro() {

    container = document.getElementById('form-carro')

    html = "<br> <div class='row'> <div class='cold-md'> <input type='text'placeholder='carro' class='form-control' name='carros'> </div> <div class='col-md'> <input type='text' placeholder='Placa' class='form-control' name='placas'> </div> <div class='col-md'> <input type='number' placeholder='ano' class='form-control' name='anos'> </div> </div >"

    container.innerHTML += html
}

function exibir_form(tipo) {

    add_cliente = document.getElementById('adicionar-cliente')
    att_cliente = document.getElementById('atualizar-cliente')

    if (tipo == '1') {
        att_cliente.style.display = "none"
        add_cliente.style.display = "block"
    }
    else if (tipo == '2') {
        add_cliente.style.display = "none"
        att_cliente.style.display = "block"
    }
}

function dados_cliente(){
    cliente = document.getElementById('cliente-select')
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
    id_cliente = cliente.value

    data = new FormData()
    data.append('id_cliente', id_cliente)

    fetch("/clientes/atualiza_cliente/",{
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: data

    }).then(function(result){
        return result.json()
    }).then(function(data){
        mostrar_att_cliente = document.querySelector('#form-att-cliente')
        mostrar_att_cliente.style.display = 'block'

        nome = document.querySelector('#nome')
        nome.value = data['cliente']['nome']

        sobrenome = document.querySelector('#sobrenome')
        sobrenome.value = data['cliente']['sobrenome']

        cpf = document.querySelector('#cpf')
        cpf.value = data['cliente']['cpf']
        
        email = document.querySelector('#email')
        email.value = data['cliente']['email']

        carros = data['carros']

        for (var i = 0; i < carros.length; i++) {
            var add_carro_html = document.querySelector('#add-carro')
            add_carro_html.innerHTML = "<br> <div class='row'> <div class='cold-md'> <input type='text'placeholder='carro' class='form-control' name='carros'> </div> <div class='col-md'> <input type='text' placeholder='Placa' class='form-control' name='placas'> </div> <div class='col-md'> <input type='number' placeholder='ano' class='form-control' name='anos'> </div> </div >"
            console.log(carros[i]['fields']['carro'])
            carros = document.querySelector('#carros')
            carros.value = carros[i]['fields']['carro']
            placas = document.querySelector('#placas')
            anos = document.querySelector('#anos')
        }

        
    })
}