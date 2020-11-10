import React from 'react'
import CartCard from './CartCard'
import Layout from './Layout'
import { getRandomImage } from '../utils/get-random-image'
import '../assets/styles/cart-card.scss'
import axios from 'axios'
import Cookies from 'universal-cookie'

const submitRequest = async (event, items, clearCart, history) => {
  const sessionId = new Cookies().get('access_token')

  // Creating request
  let requestId = (await axios.post('http://localhost:5000/request', {
    items: items.map((item) => ({
      id: item.id,
      amount: 1
    })),
    sessionId: sessionId
  })).data
  
  // Submitting request
  await axios.patch('http://localhost:5000/request/submit', {
    request: requestId,
    sessionId: sessionId
  }).then((response) => {
    clearCart()
	history.push('/requests')
  })
}

const CartCards = ({ cart, clearCart, removeItemFromCart, history }) => {
  const sum = cart.reduce((acc, curr) => acc + Number(curr.price), 0)
  const items = cart.map((item, index) => {
    return (
      <CartCard
        item={item}
        index={index}
        image={getRandomImage()}
        removeItemFromCart={removeItemFromCart}
      />
    )
  })
  return (
    <Layout>
      {cart.length > 0 ? (
        <div>
          <p>List of products on your cart</p>
          <small>Total prices of the items:{sum.toFixed(2)} Euro</small>
        </div>
      ) : (
        ''
      )}
      {cart.length > 0 ? (
        <button className='button is-link' onClick={(event) => submitRequest(event, cart, clearCart, history)}>
          Submit request
        </button>
      ) : (
        ''
      )}
      {cart.length > 0 ? (
        <div>{items}</div>
      ) : (
        <p>You do not have items in the shopping cart.</p>
      )}
    </Layout>
  )
}

export default CartCards
