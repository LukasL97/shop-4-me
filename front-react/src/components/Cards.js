import React, { useState } from 'react'
import PropTypes from 'prop-types'
import Card from './Card'

const Cards = (props) => {
  const { addItemToCart, removeItemFromCart } = props
  const cardItems = props.data.map((item, index) => (
    <Card
      key={item.id}
      item={item}
      id={item.id}
      index={index}
      addItemToCart={addItemToCart}
      removeItemFromCart={removeItemFromCart}
    />
  ))
  return <div className='cards'>{cardItems}</div>
}

Cards.propTypes = {}

export default Cards
