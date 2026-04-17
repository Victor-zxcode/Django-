import React from 'react'
import ReactDOM from 'react-dom/client'

export { default as ProductCard } from './components/ProductCard'
export { default as ProductGrid } from './components/ProductGrid'
export { default as Cart } from './components/Cart'
export { default as ProductFilter } from './components/ProductFilter'

// Função para renderizar componentes React em elementos Django
export function renderReactComponent(componentName, elementId, props = {}) {
  const element = document.getElementById(elementId)
  if (!element) return
  
  // Importação dinâmica de componentes
  const components = {
    ProductCard: () => import('./components/ProductCard').then(m => m.default),
    ProductGrid: () => import('./components/ProductGrid').then(m => m.default),
    Cart: () => import('./components/Cart').then(m => m.default),
    ProductFilter: () => import('./components/ProductFilter').then(m => m.default),
  }
  
  if (components[componentName]) {
    components[componentName]().then(Component => {
      const root = ReactDOM.createRoot(element)
      root.render(<Component {...props} />)
    })
  }
}

// Export para uso global
window.React = { renderReactComponent }
