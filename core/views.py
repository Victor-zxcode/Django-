from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProdutoForm, ClienteForm, PedidoForm, UsuarioForm
from .models import *

# Create your views here.

def home(request):
    produtos = Produtos.objects.all()
    return render(request, 'home.html', {'produtos': produtos})

def listar_produtos(request):
    produtos = Produtos.objects.all()
    return render(request, 'listar_produtos.html', {'produtos': produtos})


def comprar_produto(request, id):
    produto = get_object_or_404(Produtos, id=id)

    if request.method == 'POST':
        pedido = Pedido.objects.create()

        ItemPedido.objects.create(
            pedido=pedido,
            produto=produto,
            quantidade=1
        )

        return redirect('home')

    return render(request, 'comprar_produto.html', {
        'produto': produto
    })












# def criar_cliente(request):
#     if request.method == 'POST':
#         form = ClienteForm(request.POST)
#         if form.is_valid():
#             form.save()
#     else:
#         form = ClienteForm()
#     return render(request, 'criar_cliente.html', {'form': form})


# def criar_pedido(request):
#     if request.method == 'POST':
#         form = PedidoForm(request.POST)
#         if form.is_valid():
#             form.save()
#     else:
#         form = PedidoForm()
#     return render(request, 'criar_pedido.html', {'form': form})


# def criar_usuario(request):
#     if request.method == 'POST':
#         form = UsuarioForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#     else:
#         form = UsuarioForm()
#     return render(request, 'criar_usuario.html', {'form': form})


