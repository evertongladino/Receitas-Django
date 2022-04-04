from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('<int:receita_id>', receita, name='receita'),
    path('buscar', busca, name='buscar'),
    path('cria/receita', cria_receita, name='cria_receita'),
    path('deleta/<int:receita_id>', deleta_receita, name='deleta_receita'),
    path('altera/<int:receita_id>', altera_receita, name='altera_receita'),
    path('atualiza_receita', atualiza_receita, name='atualiza_receita')
]