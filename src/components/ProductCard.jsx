import React, { useState } from 'react'
import axios from 'axios'

export default function ProductCard({ produto, onAddToCart }) {
  const [loading, setLoading] = useState(false)
  const [hovering, setHovering] = useState(false)

  const handleAddToCart = async () => {
    setLoading(true)
    try {
      const response = await axios.post(`/api/carrinho/adicionar/${produto.id}/`)
      onAddToCart?.(response.data)
    } catch (error) {
      console.error('Erro ao adicionar ao carrinho:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <article 
      className="pcard pcard--visible"
      onMouseEnter={() => setHovering(true)}
      onMouseLeave={() => setHovering(false)}
    >
      <div className="pcard__media">
        {produto.imagem ? (
          <img 
            src={produto.imagem} 
            alt={produto.nome}
            className="pcard__img"
            loading="lazy"
          />
        ) : (
          <div className="pcard__placeholder">
            <svg className="pcard__placeholder-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <rect x="3" y="3" width="18" height="18" rx="2"/>
              <circle cx="8.5" cy="8.5" r="1.5"/>
              <path d="M21 15l-5-5L5 21"/>
            </svg>
          </div>
        )}
        {produto.desconto && (
          <span className="pcard__badge">-{produto.desconto}%</span>
        )}
        <div className="pcard__overlay">
          <button 
            className="btn btn--primary"
            onClick={handleAddToCart}
            disabled={loading}
          >
            {loading ? 'Adicionando...' : 'Adicionar ao Carrinho'}
          </button>
        </div>
      </div>

      <div className="pcard__body">
        <span className="pcard__cat">{produto.categoria}</span>
        <h3 className="pcard__title">
          <a href={`/produtos/${produto.id}/`}>{produto.nome}</a>
        </h3>
        <p className="pcard__desc">{produto.descricao?.substring(0, 100)}...</p>

        <div className="pcard__footer">
          <div className="pcard__pricing">
            {produto.preco_original && (
              <span className="pcard__price-old">R$ {produto.preco_original}</span>
            )}
            <span className="pcard__price">R$ {produto.preco}</span>
          </div>
          <a 
            href={`/comprar/${produto.id}/`}
            className="btn btn--primary btn--sm"
          >
            Comprar
          </a>
        </div>
      </div>
    </article>
  )
}
