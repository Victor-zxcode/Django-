import React, { useState, useEffect } from 'react'
import axios from 'axios'

export default function ProductFilter({ onFilterChange }) {
  const [categorias, setCategorias] = useState([])
  const [precoMin, setPrecoMin] = useState(0)
  const [precoMax, setPrecoMax] = useState(5000)
  const [selectedCategoria, setSelectedCategoria] = useState(null)

  useEffect(() => {
    fetchCategorias()
  }, [])

  const fetchCategorias = async () => {
    try {
      const response = await axios.get('/api/categorias/')
      setCategorias(response.data)
    } catch (error) {
      console.error('Erro ao carregar categorias:', error)
    }
  }

  const handleFilter = () => {
    onFilterChange?.({
      categoria: selectedCategoria,
      preco_min: precoMin,
      preco_max: precoMax
    })
  }

  return (
    <div className="filtros">
      <div className="filtro-group">
        <label className="form-label">Categoria</label>
        <select 
          className="form-input"
          value={selectedCategoria || ''}
          onChange={(e) => setSelectedCategoria(e.target.value || null)}
        >
          <option value="">Todas</option>
          {categorias.map(cat => (
            <option key={cat.id} value={cat.slug}>{cat.nome}</option>
          ))}
        </select>
      </div>

      <div className="filtro-group">
        <label className="form-label">Preço: R$ {precoMin} - R$ {precoMax}</label>
        <input 
          type="range" 
          min="0" 
          max="5000" 
          value={precoMax}
          onChange={(e) => setPrecoMax(parseInt(e.target.value))}
          className="form-input"
        />
      </div>

      <button className="btn btn--primary btn--full" onClick={handleFilter}>
        Filtrar
      </button>
    </div>
  )
}
