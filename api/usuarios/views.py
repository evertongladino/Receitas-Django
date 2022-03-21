from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita

def cadastro(request):
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
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    if request.user.is_authenticated:
        receitas = Receita.objects.order_by('-date').filter(autor=request.user.id)

        dados = {
            'receitas':receitas
        }

        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')

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
        return render(request, 'usuarios/cria_receita.html')

def campo_vazio(campo):
    return not campo.strip()

def valida_senha(senha, senha2):
    return senha != senha2