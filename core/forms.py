from django.forms import ModelForm
from .models import Produtos, Clientes, Pedido, Usuario


class ProdutoForm(ModelForm):
    class Meta:
        model = Produtos
        fields = '__all__'

class ClienteForm(ModelForm):
    class Meta:
        model = Clientes
        fields = '__all__'

class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'

class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'

