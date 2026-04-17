# TechStore - React Integration Guide

## Setup React com Django

O projeto foi migrado para usar React com Vite. Siga os passos abaixo para configurar:

### 1. Instalar Dependências

```bash
npm install
```

### 2. Arquitetura

- **Vite**: Bundler e dev server
- **React 18**: UI framework
- **Zustand**: State management
- **Axios**: HTTP client para API calls

### 3. Estrutura de Diretórios

```
src/
├── main.jsx              # Entry point
├── components/           # Componentes React reutilizáveis
│   ├── ProductCard.jsx   # Card de produto
│   ├── ProductGrid.jsx   # Grid de produtos
│   ├── ProductFilter.jsx # Filtros de produtos
│   └── Cart.jsx          # Carrinho de compras
└── pages/               # Páginas React
    ├── produtos.jsx     # Página de produtos
    └── carrinho.jsx     # Página do carrinho
```

### 4. Desenvolvimento

#### Terminal 1 - Django:
```bash
python manage.py runserver 8000
```

#### Terminal 2 - Vite (React):
```bash
npm run dev
```

Isso inicia o dev server do Vite na porta 5173 com hot reload.

### 5. Build para Produção

```bash
npm run build
```

Arquivos compilados em: `core/static/js/dist/`

### 6. Integrar Componentes React em Templates Django

#### Opção A: Com Vite HMR (Desenvolvimento)

```html
<div id="app"></div>
<script type="module" src="http://localhost:5173/src/main.jsx"></script>
```

#### Opção B: Com Build Estático (Produção)

```html
<div id="app"></div>
{% load static %}
<script src="{% static 'js/dist/main.js' %}"></script>
```

### 7. Usar Componentes Específicos

```html
<!-- Em um template Django -->
<div id="produto-grid"></div>

<script>
  React.renderReactComponent('ProductGrid', 'produto-grid', {
    categoriaSlug: '{{ categoria.slug }}',
    busca: '{{ busca }}'
  })
</script>
```

### 8. API Endpoints Necessários

Django deve expor estes endpoints:

```
GET    /api/produtos/              - Lista de produtos
GET    /api/produtos/{id}/         - Detalhe do produto
GET    /api/categorias/            - Lista de categorias
POST   /api/carrinho/adicionar/    - Adicionar ao carrinho
GET    /api/carrinho/              - Ver carrinho
DELETE /api/carrinho/remover/{id}/ - Remover do carrinho
PATCH  /api/carrinho/{id}/         - Atualizar quantidade
```

### 9. Próximos Passos

1. Criar app Django `rest_framework` com API endpoints
2. Integrar React em templates específicas (produtos, carrinho)
3. Configurar CORS se necessário
4. Adicionar autenticação com JWT
5. Implementar mais componentes (checkout, conta do usuário, etc)

### 10. Variáveis de Ambiente

Criar `.env.local`:

```
VITE_API_URL=http://localhost:8000
VITE_API_KEY=seu_token_aqui
```

Usar em componentes:

```javascript
const API_URL = import.meta.env.VITE_API_URL
```

### Troubleshooting

#### CORS Error
Adicionar em `django1/settings.py`:
```python
INSTALLED_APPS += ['corsheaders']
MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')
CORS_ALLOWED_ORIGINS = ['http://localhost:5173']
```

#### Hot Reload não funciona
Certificar que Vite está rodando na porta 5173 e que está acessível de `localhost`

#### Módulos não encontrados
```bash
npm install
rm -rf node_modules
npm install
```

## Componentes Disponíveis

### ProductCard
```jsx
<ProductCard 
  produto={produtoObj}
  onAddToCart={(data) => console.log(data)}
/>
```

### ProductGrid
```jsx
<ProductGrid 
  categoriaSlug="eletronicos"
  busca="iphone"
/>
```

### ProductFilter
```jsx
<ProductFilter 
  onFilterChange={(filters) => console.log(filters)}
/>
```

### Cart
```jsx
<Cart />
```

## Performance

- Code splitting automático com Vite
- Lazy loading de componentes
- CSS-in-JS otimizado
- Caching de API com Zustand

---

**Status**: ✅ Setup completo e pronto para desenvolvimento!
