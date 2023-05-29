from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='clientes'),
    path('atualiza_cliente_id/', views.att_cliente_id, name='atualiza_cliente_id'),
    path('atualiza_cliente/', views.att_cliente, name='atualiza_cliente'),
    path('update_cliente/<int:id>', views.update_cliente, name='atualiza_cliente_cadastrado'),
    path('update_carro/<int:id>', views.update_carro, name='update_carro'),
    path('excluir_carro/<int:id>', views.excluir_carro, name='excluir_carro')
]