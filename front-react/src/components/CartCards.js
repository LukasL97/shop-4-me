import React from 'react'
import CartCard from './CartCard'
import Layout from './Layout'
import { getRandomImage } from '../utils/get-random-image'
import '../assets/styles/cart-card.scss'

const CartCards = ({ cart, removeItemFromCart }) => {
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
          <small>Total prices of the items:{sum} Euro</small>
        </div>
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
