from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    CategoriaViewSet, ProdutoViewSet, CarrinhoViewSet,
    ItemCarrinhoViewSet, PedidoViewSet
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'produtos', ProdutoViewSet, basename='produto')
router.register(r'carrinho/itens', ItemCarrinhoViewSet, basename='carrinho-item')
router.register(r'carrinho', CarrinhoViewSet, basename='carrinho')
router.register(r'pedidos', PedidoViewSet, basename='pedido')

urlpatterns = [
    path('', include(router.urls)),
]
