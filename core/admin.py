from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Produto, Categoria, Pedido, ItemPedido, Carrinho, ItemCarrinho


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    pass


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display        = ['nome', 'icone', 'ativa', 'ordem']
    list_editable       = ['ativa', 'ordem']
    prepopulated_fields = {'slug': ('nome',)}


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display        = ['nome', 'categoria', 'preco', 'status', 'destaque', 'criado_em']
    list_filter         = ['status', 'destaque', 'categoria']
    search_fields       = ['nome', 'descricao']
    prepopulated_fields = {'slug': ('nome',)}
    list_editable       = ['status', 'destaque']
    ordering            = ['-criado_em']


class ItemPedidoInline(admin.TabularInline):
    model  = ItemPedido
    extra  = 0
    fields = ['produto', 'preco']
    readonly_fields = ['preco']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display    = ['id', 'usuario', 'status', 'total', 'criado_em']
    list_filter     = ['status']
    search_fields   = ['usuario__username']
    readonly_fields = ['total', 'criado_em', 'atualizado_em']
    inlines         = [ItemPedidoInline]


class ItemCarrinhoInline(admin.TabularInline):
    model  = ItemCarrinho
    extra  = 0
    fields = ['produto']

@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'quantidade_itens', 'total', 'atualizado_em']
    inlines      = [ItemCarrinhoInline]