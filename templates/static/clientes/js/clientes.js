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
        console.log(data)
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
        var add_carro_html = document.querySelector('#altera-carro')
        add_carro_html.innerHTML = ''
        for (var i = 0; i < carros.length; i++) {
            add_carro_html.innerHTML += "<br>\
            <form method='POST' action='/clientes/update_carro/"+carros[i]['id']+"'>\
                <div class='row'>\
                    <div class='cold-md'>\
                        <input type='text'placeholder='carro' class='form-control' name='carros' value='"+carros[i]['fields']['carro']+"'>\
                    </div>\
                    <div class='col-md'>\
                        <input type='text' placeholder='Placa' class='form-control' name='placas' value='"+carros[i]['fields']['placa']+"'>\
                    </div>\
                    <div class='col-md'>\
                        <input type='number' placeholder='ano' class='form-control' name='anos' value='"+carros[i]['fields']['ano']+"'>\
                    </div>\
                    <div class='col-md'>\
                        <input class='btn btn-success' type='submit' value'Submeter pedido'>\
                    </div>\
                    <div class='col-md'>\
                        <a class='btn btn-danger' href='/clientes/excluir_carro/"+carros[i]['id']+"' >Excluir</a>\
                    </div>\
                </div >\
            </form>"
        }
    })
}

function update_cliente() {
    nome = document.querySelector('#nome').value
    sobrenome = document.querySelector('#sobrenome').value
    email = document.querySelector('#email').value
    cpf = document.querySelector('#cpf').value
    id = document.querySelector('#cliente-select').value

    fetch('/clientes/update_cliente/'+id, {
        method : 'POST',
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({
            nome: nome,
            sobrenome : sobrenome,
            email : email,
            cpf : cpf,
        })
    }
    ).then(function(result){
        return result.json()
    }).then(function(data){
        var alerta_tela = document.querySelector('#alerta-cliente')
        if (data['status'] == '200') {
            nome = data['nome']
            sobrenome = data['sobrenome']
            email = data['email']
            cpf = data['cpf']
            alerta_tela.innerHTML = "\
            <div class='alert alert-success' role='alert'>\
                Dados alterados com sucesso!\
            </div>"
            alerta_tela.style.display = 'block'
        } else {
            alerta_tela.innerHTML = "\
            <div class='alert alert-danger' role='alert'>\
                Algo seu errado, verifique os campos e tente novamente!\
            </div>"
            alerta_tela.style.display = 'block'

        }
    })
}