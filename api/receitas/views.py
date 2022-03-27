from cgitb import html
from django.shortcuts import render, redirect, get_object_or_404
from .models import Receita
from django.contrib.auth.models import User
from django.contrib import auth, messages

def index(request):
    receitas = Receita.objects.order_by('-date').filter(publicada=True)

    dados = {
        'receitas': receitas
    }

    return render(request, 'receitas/index.html', dados)

def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)

    receita_a_exibir = {
        'receita': receita
    }

    return render(request, 'receitas/receita.html', receita_a_exibir)

def buscar(request):
    lista_receitas = Receita.objects.order_by('-date').filter(publicada=True)
    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        if buscar:
            lista_receitas = lista_receitas.filter(nome_receita__icontains=nome_a_buscar)

    dados = {
        'receitas': lista_receitas
    }
    return render(request, 'receitas/buscar.html', dados)

def cria_receita(request):
    if request.method == 'POST':
        nome_receita= request.POST['nome_receita']
        ingredientes= request.POST['ingredientes']
        modo_preparo= request.POST['modo_preparo']
        tempo_preparo= request.POST['tempo_preparo']
        rendimento= request.POST['rendimento']
        categoria= request.POST['categoria']
        foto_receita= request.FILES['foto_receita']
        print(nome_receita,ingredientes,modo_preparo,tempo_preparo,rendimento,categoria, foto_receita)
        user = get_object_or_404(User, pk=request.user.id)
        receita = Receita.objects.create(autor=user,nome_receita=nome_receita,ingredientes=ingredientes,modo_de_preparo=modo_preparo
        , tempo_de_preparo=tempo_preparo,rendimento=rendimento,foto_publicada=foto_receita)
        receita.save()
        return redirect('dashboard')
    else:
        return render(request, 'receitas/cria_receita.html')

def deleta_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    return redirect('dashboard')

def altera_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_alterar = { 'receita' : receita }
    return render(request,'receitas/altera_receita.html', receita_a_alterar)

def atualiza_receita(request):
    if request.method == 'POST':
        receita_id = request.POST['receita_id']
        r = Receita.objects.get(pk=receita_id)
        r.nome_receita = request.POST['nome_receita']
        r.ingredientes = request.POST['ingredientes']
        r.modo_de_preparo = request.POST['modo_preparo']
        r.tempo_de_preparo = request.POST['tempo_preparo']
        r.rendimento = request.POST['rendimento']
        r.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES:
            r.foto_publicada = request.FILES['foto_receita']
        if campo_vazio(r.nome_receita):
            messages.error(request, 'O nome da receita não pode ser vazio!')
            return redirect('atualiza_receita')
        r.save()
    return redirect('dashboard')

def campo_vazio(campo):
    return not campo.strip()