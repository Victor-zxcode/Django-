from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Q
from .models import Usuario, Produto, Categoria, Pedido, ItemPedido, Carrinho, ItemCarrinho


class BaseAdmin(admin.ModelAdmin):
    class Media:
        css = {'all': ('css/admin_custom.css',)}


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('username', 'email', 'first_name', 'last_name')
        }),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Datas', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

    list_display = ('username', 'email', 'nome_completo', 'status_badge', 'data_registro')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('last_login', 'date_joined')

    def nome_completo(self, obj):
        return obj.get_full_name() or obj.username
    nome_completo.short_description = 'Nome Completo'

    def status_badge(self, obj):
        if obj.is_superuser:
            cor = '#3B37CC'
            texto = '👑 Admin'
        elif obj.is_staff:
            cor = '#FF6B35'
            texto = '👤 Staff'
        else:
            cor = '#16A34A'
            texto = '✓ Ativo' if obj.is_active else '✗ Inativo'
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 600;">{}</span>',
            cor, texto
        )
    status_badge.short_description = 'Status'

    def data_registro(self, obj):
        return obj.date_joined.strftime('%d/%m/%Y %H:%M')
    data_registro.short_description = 'Registrado em'


@admin.register(Categoria)
class CategoriaAdmin(BaseAdmin):
    fieldsets = (
        ('Informações', {
            'fields': ('nome', 'slug', 'ordem')
        }),
        ('Exibição', {
            'fields': ('ativa', 'icone', 'icone_lucide')
        }),
    )

    list_display = ('nome', 'quantidade_produtos', 'ordem', 'ativa_badge', 'icone_preview')
    list_filter = ('ativa', 'ordem')
    search_fields = ('nome', 'slug')
    prepopulated_fields = {'slug': ('nome',)}
    list_editable = ('ordem',)
    ordering = ('ordem', 'nome')

    def quantidade_produtos(self, obj):
        count = obj.produtos.filter(status='ativo').count()
        return format_html(
            '<span style="background-color: #EEEEFF; color: #3B37CC; padding: 4px 10px; border-radius: 4px; font-weight: 600;">{}</span>',
            count
        )
    quantidade_produtos.short_description = 'Produtos Ativos'

    def ativa_badge(self, obj):
        if obj.ativa:
            return format_html(
                '<span style="color: #16A34A; font-weight: 600;">✓ Ativa</span>'
            )
        return format_html(
            '<span style="color: #DC2626; font-weight: 600;">✗ Inativa</span>'
        )
    ativa_badge.short_description = 'Status'

    def icone_preview(self, obj):
        return obj.icone_lucide or '—'
    icone_preview.short_description = 'Ícone'


@admin.register(Produto)
class ProdutoAdmin(BaseAdmin):
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'slug', 'categoria', 'status')
        }),
        ('Descrição', {
            'fields': ('resumo', 'descricao')
        }),
        ('Preço e Desconto', {
            'fields': ('preco', 'preco_original', 'percentual_desconto_display')
        }),
        ('Imagem', {
            'fields': ('imagem', 'imagem_preview')
        }),
        ('Destaque e Datas', {
            'fields': ('destaque', 'criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )

    list_display = (
        'nome_truncado',
        'categoria',
        'preco_display',
        'status_badge',
        'desconto_badge',
        'destaque_badge',
        'imagem_thumb'
    )
    list_filter = ('status', 'destaque', 'categoria', 'criado_em')
    search_fields = ('nome', 'descricao', 'slug')
    prepopulated_fields = {'slug': ('nome',)}
    readonly_fields = ('criado_em', 'atualizado_em', 'imagem_preview', 'percentual_desconto_display')
    ordering = ('-criado_em',)

    def nome_truncado(self, obj):
        nome = obj.nome[:50] + '...' if len(obj.nome) > 50 else obj.nome
        return nome
    nome_truncado.short_description = 'Produto'

    def preco_display(self, obj):
        if obj.preco_original and obj.preco_original > obj.preco:
            return format_html(
                '<span style="color: #16A34A; font-weight: 600;">R$ {:.2f}</span><br/>'
                '<span style="text-decoration: line-through; color: #9E9BA8; font-size: 11px;">R$ {:.2f}</span>',
                obj.preco, obj.preco_original
            )
        return format_html(
            '<span style="color: #1A1A2E; font-weight: 600;">R$ {:.2f}</span>',
            obj.preco
        )
    preco_display.short_description = 'Preço'

    def status_badge(self, obj):
        status_colors = {
            'ativo': ('#16A34A', '✓ Ativo'),
            'inativo': ('#DC2626', '✗ Inativo'),
            'rascunho': ('#D97706', '📝 Rascunho'),
        }
        cor, texto = status_colors.get(obj.status, ('#9E9BA8', obj.status))
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; border-radius: 4px; font-weight: 600; font-size: 11px;">{}</span>',
            cor, texto
        )
    status_badge.short_description = 'Status'

    def desconto_badge(self, obj):
        if obj.tem_desconto:
            return format_html(
                '<span style="background-color: #FF6B35; color: white; padding: 4px 10px; border-radius: 4px; font-weight: 600; font-size: 11px;">-{}%</span>',
                obj.percentual_desconto
            )
        return '—'
    desconto_badge.short_description = 'Desconto'

    def destaque_badge(self, obj):
        if obj.destaque:
            return format_html(
                '<span style="color: #FF6B35; font-weight: 600; font-size: 16px;">⭐</span>'
            )
        return '—'
    destaque_badge.short_description = 'Destaque'

    def imagem_thumb(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 4px; object-fit: cover;" />',
                obj.imagem.url
            )
        return '—'
    imagem_thumb.short_description = 'Imagem'

    def imagem_preview(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" style="max-width: 300px; border-radius: 8px;" />',
                obj.imagem.url
            )
        return 'Sem imagem'
    imagem_preview.short_description = 'Prévia da Imagem'

    def percentual_desconto_display(self, obj):
        if obj.tem_desconto:
            return f'{obj.percentual_desconto}%'
        return '—'
    percentual_desconto_display.short_description = 'Percentual de Desconto'


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    fields = ('produto', 'preco_display', 'preco')
    readonly_fields = ('preco_display',)
    can_delete = True

    def preco_display(self, obj):
        return format_html(
            '<strong>R$ {:.2f}</strong>',
            obj.preco
        )
    preco_display.short_description = 'Preço (Informativo)'


@admin.register(Pedido)
class PedidoAdmin(BaseAdmin):
    fieldsets = (
        ('Cliente', {
            'fields': ('usuario', 'total')
        }),
        ('Status do Pedido', {
            'fields': ('status',)
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )

    list_display = ('pedido_id', 'usuario', 'total_display', 'status_badge', 'data_pedido', 'itens_count')
    list_filter = ('status', 'criado_em')
    search_fields = ('usuario__username', 'usuario__email', 'id')
    readonly_fields = ('total', 'criado_em', 'atualizado_em')
    inlines = (ItemPedidoInline,)
    ordering = ('-criado_em',)

    def pedido_id(self, obj):
        return format_html(
            '<strong>Pedido #{}</strong>',
            obj.id
        )
    pedido_id.short_description = 'ID'

    def total_display(self, obj):
        return format_html(
            '<span style="color: #16A34A; font-weight: 600; font-size: 13px;">R$ {:.2f}</span>',
            obj.total
        )
    total_display.short_description = 'Total'

    def status_badge(self, obj):
        status_colors = {
            'pendente': '#D97706',
            'pago': '#16A34A',
            'cancelado': '#DC2626',
        }
        cor = status_colors.get(obj.status, '#9E9BA8')
        status_labels = {
            'pendente': '⏳ Pendente',
            'pago': '✓ Pago',
            'cancelado': '✗ Cancelado',
        }
        texto = status_labels.get(obj.status, obj.status)
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 4px; font-weight: 600; font-size: 11px;">{}</span>',
            cor, texto
        )
    status_badge.short_description = 'Status'

    def data_pedido(self, obj):
        return obj.criado_em.strftime('%d/%m/%Y %H:%M')
    data_pedido.short_description = 'Data'

    def itens_count(self, obj):
        count = obj.itens.count()
        return format_html(
            '<span style="background-color: #EEEEFF; color: #3B37CC; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 11px;">{} item(ns)</span>',
            count
        )
    itens_count.short_description = 'Itens'


class ItemCarrinhoInline(admin.TabularInline):
    model = ItemCarrinho
    extra = 0
    fields = ('produto', 'preco_display')
    readonly_fields = ('preco_display',)

    def preco_display(self, obj):
        return format_html(
            '<strong>R$ {:.2f}</strong>',
            obj.produto.preco
        )
    preco_display.short_description = 'Preço'


@admin.register(Carrinho)
class CarrinhoAdmin(BaseAdmin):
    fieldsets = (
        ('Cliente', {
            'fields': ('usuario', 'total_display', 'quantidade_itens_display')
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )

    list_display = ('usuario', 'total_display', 'quantidade_itens_display', 'data_atualizacao', 'sem_itens')
    list_filter = ('criado_em', 'atualizado_em')
    search_fields = ('usuario__username', 'usuario__email')
    readonly_fields = ('total_display', 'quantidade_itens_display', 'criado_em', 'atualizado_em')
    inlines = (ItemCarrinhoInline,)
    ordering = ('-atualizado_em',)
    can_delete = True

    def total_display(self, obj):
        total = obj.total
        return format_html(
            '<span style="color: #FF6B35; font-weight: 600;">R$ {:.2f}</span>',
            total
        )
    total_display.short_description = 'Total'

    def quantidade_itens_display(self, obj):
        count = obj.quantidade_itens
        return format_html(
            '<span style="background-color: #FFF1EC; color: #FF6B35; padding: 4px 8px; border-radius: 4px; font-weight: 600;">{}</span>',
            count
        )
    quantidade_itens_display.short_description = 'Itens'

    def data_atualizacao(self, obj):
        return obj.atualizado_em.strftime('%d/%m/%Y %H:%M')
    data_atualizacao.short_description = 'Atualizado em'

    def sem_itens(self, obj):
        if obj.quantidade_itens == 0:
            return format_html(
                '<span style="color: #D97706; font-weight: 600;">📦 Vazio</span>'
            )
        return '—'
    sem_itens.short_description = 'Info'
    list_display = ['usuario', 'quantidade_itens', 'total', 'atualizado_em']
    inlines      = [ItemCarrinhoInline]