from rest_framework import serializers
from .models import Categoria, Produto, Carrinho, ItemCarrinho, Pedido, ItemPedido


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'slug', 'icone_lucide', 'ativa', 'ordem']


class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    categoria_slug = serializers.CharField(source='categoria.slug', read_only=True)

    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'slug', 'descricao', 'preco', 'preco_original',
            'imagem', 'status', 'categoria', 'categoria_nome', 'categoria_slug',
            'criado_em', 'atualizado_em'
        ]


class ItemCarrinhoSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer(read_only=True)
    produto_id = serializers.IntegerField(write_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItemCarrinho
        fields = ['id', 'produto', 'produto_id', 'quantidade', 'adicionado_em', 'subtotal']

    def get_subtotal(self, obj):
        return obj.produto.preco * obj.quantidade


class CarrinhoSerializer(serializers.ModelSerializer):
    itens = ItemCarrinhoSerializer(
        source='itemcarrinho_set',
        many=True,
        read_only=True
    )
    total = serializers.SerializerMethodField()
    quantidade_itens = serializers.SerializerMethodField()

    class Meta:
        model = Carrinho
        fields = ['id', 'usuario', 'itens', 'total', 'quantidade_itens', 'criado_em']

    def get_total(self, obj):
        return sum(
            item.produto.preco * item.quantidade
            for item in obj.itemcarrinho_set.all()
        )

    def get_quantidade_itens(self, obj):
        return obj.itemcarrinho_set.count()


class ItemPedidoSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer(read_only=True)

    class Meta:
        model = ItemPedido
        fields = ['id', 'produto', 'quantidade', 'preco']


class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(
        source='itempedido_set',
        many=True,
        read_only=True
    )
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)

    class Meta:
        model = Pedido
        fields = [
            'id', 'usuario', 'usuario_email', 'status', 'total',
            'itens', 'criado_em', 'atualizado_em'
        ]
