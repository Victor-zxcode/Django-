from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Categoria, Produto, Carrinho, ItemCarrinho, Pedido, ItemPedido
from .serializers import (
    CategoriaSerializer, ProdutoSerializer, CarrinhoSerializer,
    ItemCarrinhoSerializer, PedidoSerializer, ItemPedidoSerializer
)


class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.filter(ativa=True).order_by('ordem')
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.query_params.get('nome')
        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        return queryset


class ProdutoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Produto.objects.filter(status='ATIVO').order_by('-criado_em')
    serializer_class = ProdutoSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        categoria = self.request.query_params.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria__slug=categoria)

        busca = self.request.query_params.get('busca')
        if busca:
            queryset = queryset.filter(
                Q(nome__icontains=busca) | Q(descricao__icontains=busca)
            )

        preco_min = self.request.query_params.get('preco_min')
        preco_max = self.request.query_params.get('preco_max')
        if preco_min:
            queryset = queryset.filter(preco__gte=float(preco_min))
        if preco_max:
            queryset = queryset.filter(preco__lte=float(preco_max))

        ordenacao = self.request.query_params.get('ordenacao', '-criado_em')
        queryset = queryset.order_by(ordenacao)

        return queryset


class ItemCarrinhoViewSet(viewsets.ModelViewSet):
    serializer_class = ItemCarrinhoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        carrinho, _ = Carrinho.objects.get_or_create(usuario=self.request.user)
        return carrinho.itemcarrinho_set.all()

    def perform_create(self, serializer):
        carrinho, _ = Carrinho.objects.get_or_create(usuario=self.request.user)
        serializer.save(carrinho=carrinho)


class CarrinhoViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        carrinho, _ = Carrinho.objects.get_or_create(usuario=request.user)
        serializer = CarrinhoSerializer(carrinho)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def adicionar_item(self, request):
        produto_id = request.data.get('produto_id')
        quantidade = request.data.get('quantidade', 1)

        produto = get_object_or_404(Produto, id=produto_id)
        carrinho, _ = Carrinho.objects.get_or_create(usuario=request.user)

        item, created = ItemCarrinho.objects.get_or_create(
            carrinho=carrinho,
            produto=produto,
            defaults={'quantidade': quantidade}
        )

        if not created:
            item.quantidade += int(quantidade)
            item.save()

        serializer = CarrinhoSerializer(carrinho)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def remover_item(self, request):
        item_id = request.data.get('item_id')
        item = get_object_or_404(ItemCarrinho, id=item_id)

        if item.carrinho.usuario != request.user:
            return Response(
                {'erro': 'Não autorizado'},
                status=status.HTTP_403_FORBIDDEN
            )

        item.delete()

        carrinho = Carrinho.objects.get(usuario=request.user)
        serializer = CarrinhoSerializer(carrinho)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def atualizar_item(self, request):
        item_id = request.data.get('item_id')
        quantidade = request.data.get('quantidade')

        item = get_object_or_404(ItemCarrinho, id=item_id)

        if item.carrinho.usuario != request.user:
            return Response(
                {'erro': 'Não autorizado'},
                status=status.HTTP_403_FORBIDDEN
            )

        if quantidade and int(quantidade) > 0:
            item.quantidade = int(quantidade)
            item.save()
        else:
            item.delete()

        carrinho = Carrinho.objects.get(usuario=request.user)
        serializer = CarrinhoSerializer(carrinho)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def limpar(self, request):
        carrinho, _ = Carrinho.objects.get_or_create(usuario=request.user)
        carrinho.itemcarrinho_set.all().delete()
        serializer = CarrinhoSerializer(carrinho)
        return Response(serializer.data)


class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user).order_by('-criado_em')

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=['post'])
    def criar_do_carrinho(self, request):
        carrinho = get_object_or_404(Carrinho, usuario=request.user)

        if not carrinho.itemcarrinho_set.exists():
            return Response(
                {'erro': 'Carrinho vazio'},
                status=status.HTTP_400_BAD_REQUEST
            )

        total = sum(
            item.produto.preco * item.quantidade
            for item in carrinho.itemcarrinho_set.all()
        )

        pedido = Pedido.objects.create(
            usuario=request.user,
            status='PENDENTE',
            total=total
        )

        for item in carrinho.itemcarrinho_set.all():
            ItemPedido.objects.create(
                pedido=pedido,
                produto=item.produto,
                quantidade=item.quantidade,
                preco=item.produto.preco
            )

        carrinho.itemcarrinho_set.all().delete()

        serializer = PedidoSerializer(pedido)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
