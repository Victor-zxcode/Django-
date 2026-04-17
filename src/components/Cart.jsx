import React, { useState, useEffect } from 'react'
import axios from 'axios'

export default function Cart() {
  const [itens, setItens] = useState([])
  const [loading, setLoading] = useState(true)
  const [total, setTotal] = useState(0)

  useEffect(() => {
    fetchCarrinho()
  }, [])

  useEffect(() => {
    calcularTotal()
  }, [itens])

  const fetchCarrinho = async () => {
    try {
      const response = await axios.get('/api/carrinho/')
      setItens(response.data.itens || [])
    } catch (error) {
      console.error('Erro ao carregar carrinho:', error)
    } finally {
      setLoading(false)
    }
  }

  const calcularTotal = () => {
    const soma = itens.reduce((acc, item) => acc + (item.preco * item.quantidade), 0)
    setTotal(soma)
  }

  const removerItem = async (itemId) => {
    try {
      await axios.delete(`/api/carrinho/remover/${itemId}/`)
      fetchCarrinho()
    } catch (error) {
      console.error('Erro ao remover item:', error)
    }
  }

  const atualizarQuantidade = async (itemId, novaQtd) => {
    try {
      await axios.patch(`/api/carrinho/${itemId}/`, { quantidade: novaQtd })
      fetchCarrinho()
    } catch (error) {
      console.error('Erro ao atualizar quantidade:', error)
    }
  }

  if (loading) return <div className="loader">Carregando carrinho...</div>

  if (itens.length === 0) {
    return (
      <div className="lista-vazio">
        <h3>Seu carrinho está vazio</h3>
        <p>Adicione produtos para começar suas compras</p>
        <a href="/produtos" className="btn btn--primary">Ver Produtos</a>
      </div>
    )
  }

  return (
    <div className="carrinho-container">
      <div className="carrinho-itens">
        {itens.map(item => (
          <div key={item.id} className="carrinho-item">
            <img src={item.produto.imagem} alt={item.produto.nome} />
            <div className="carrinho-item-info">
              <h4>{item.produto.nome}</h4>
              <p>R$ {item.preco}</p>
            </div>
            <div className="carrinho-item-quantidade">
              <button onClick={() => atualizarQuantidade(item.id, item.quantidade - 1)}>-</button>
              <span>{item.quantidade}</span>
              <button onClick={() => atualizarQuantidade(item.id, item.quantidade + 1)}>+</button>
            </div>
            <div className="carrinho-item-total">
              R$ {(item.preco * item.quantidade).toFixed(2)}
            </div>
            <button 
              className="btn btn--ghost btn--sm"
              onClick={() => removerItem(item.id)}
            >
              Remover
            </button>
          </div>
        ))}
      </div>

      <div className="carrinho-resumo">
        <h3>Resumo</h3>
        <div className="resumo-linha">
          <span>Subtotal:</span>
          <span>R$ {total.toFixed(2)}</span>
        </div>
        <div className="resumo-linha">
          <span>Frete:</span>
          <span>R$ 0,00</span>
        </div>
        <div className="resumo-linha resumo-total">
          <span>Total:</span>
          <span>R$ {total.toFixed(2)}</span>
        </div>
        <a href="/checkout" className="btn btn--primary btn--full">
          Prosseguir para Checkout
        </a>
      </div>
    </div>
  )
}
