from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita

def cadastro(request):
    """Cadastra uma nova pessoa no sistema """
    if request.method == 'POST':
        nome = request.POST['nome']
        user_name = request.POST['user_name']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if campo_vazio(nome):
            messages.error(request, 'Campo nome não pode ser vazio!')
            return redirect('cadastro')
        if campo_vazio(user_name):
            messages.error(request, 'Campo username não pode ser vazio!')
            return redirect('cadastro')
        if campo_vazio(email):
            messages.error(request, 'Campo email não pode ser vazio!')
            return redirect('cadastro')
        if valida_senha(senha, senha2):
            messages.error(request, 'As senhas devem ser iguais!')
            return redirect('cadastro')
        if User.objects.filter(username=user_name).exists():
            messages.error(request, 'Usuário já existe!')
            return redirect('cadastro')
        user = User.objects.create_user(username=user_name, first_name=nome,email=email, password=senha)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    """Realiza o login no sistema"""
    if request.method == 'POST':
        user_name = request.POST['user_name']
        senha = request.POST['senha']
        if campo_vazio(user_name) or campo_vazio(senha):
            messages.error(request, 'Todos os campos são obrigatórios')
            return redirect('login')
        if User.objects.filter(username=user_name).exists():
            #nome = User.objects.filter(username=user_name).values_list('username', flat=True).get()
            user = auth.authenticate(request,username=user_name,password=senha)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
    return render(request, 'usuarios/login.html')

def logout(request):
    """Desloga o usuario do sistema"""
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    """Busca receitas do usuario, ordenando por data e envia para o template dashboard"""
    if request.user.is_authenticated:
        receitas = Receita.objects.order_by('-date').filter(autor=request.user.id)

        dados = {
            'receitas':receitas
        }

        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')

def campo_vazio(campo):
    """No cadastro, checa se o campo é vazio"""
    return not campo.strip()

def valida_senha(senha, senha2):
    """Verifica se as senhas solicitadas no cadastro são iguais """
    return senha != senha2