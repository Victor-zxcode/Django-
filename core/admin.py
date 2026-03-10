from django.contrib import admin
from .models import Produtos, Clientes, Pedidos, Usuario

# Register your models here.

# admin.site.register(Produtos)
@admin.register(Produtos)
class ProdutosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque')
    search_fields = ('nome',)
    list_filter = ('preco',)

# admin.site.register(Clientes)
@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone')
    search_fields = ('nome', 'email')
    list_filter = ('nome',)

# admin.site.register(Pedidos)
@admin.register(Pedidos)
class PedidosAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'produto', 'quantidade', 'data_pedido')
    search_fields = ('cliente__nome', 'produto__nome')
    list_filter = ('data_pedido',)

# admin.site.register(Usuario)
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'telefone', 'cpf')
    search_fields = ('username', 'email')
    list_filter = ('username',)

