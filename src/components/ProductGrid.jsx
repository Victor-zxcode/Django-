import React, { useState, useEffect } from 'react'
import ProductCard from './ProductCard'
import axios from 'axios'

export default function ProductGrid({ categoriaSlug = null, busca = '' }) {
  const [produtos, setProdutos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchProdutos()
  }, [categoriaSlug, busca])

  const fetchProdutos = async () => {
    setLoading(true)
    try {
      let url = '/api/produtos/'
      const params = new URLSearchParams()
      
      if (categoriaSlug) params.append('categoria', categoriaSlug)
      if (busca) params.append('busca', busca)
      
      if (params.toString()) url += `?${params.toString()}`
      
      const response = await axios.get(url)
      setProdutos(response.data.results || response.data)
      setError(null)
    } catch (err) {
      setError('Erro ao carregar produtos')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="products__grid">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="skeleton pcard" style={{ height: '400px' }} />
        ))}
      </div>
    )
  }

  if (error) {
    return <div className="lista-vazio"><p>{error}</p></div>
  }

  if (produtos.length === 0) {
    return (
      <div className="lista-vazio">
        <div className="lista-vazio__icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z"/>
          </svg>
        </div>
        <h3>Nenhum produto encontrado</h3>
        <p>Tente ajustar seus filtros ou busca</p>
      </div>
    )
  }

  return (
    <div className="products__grid">
      {produtos.map((produto, index) => (
        <ProductCard 
          key={produto.id} 
          produto={produto}
          onAddToCart={() => fetchProdutos()}
        />
      ))}
    </div>
  )
}
