from django.contrib import admin
from .models import *

@admin.register(Produtos)
class ProdutosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'preco', 'mostrar_estoque')

    def mostrar_estoque(self, obj):
        if hasattr(obj, "estoque"):
            return obj.estoque.quantidade
        return 0

    mostrar_estoque.short_description = "Estoque"


@admin.register(Estoques)
class EstoquesAdmin(admin.ModelAdmin):
    list_display = ('produto', 'quantidade')
    search_fields = ('produto__nome',)
    list_filter = ('quantidade',)


@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone')
    search_fields = ('nome', 'email')
    list_filter = ('nome',)


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'criado_em')
    inlines = [ItemPedidoInline]


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'telefone', 'cpf')
    search_fields = ('username', 'email')
    list_filter = ('username',)