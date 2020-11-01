import React, { useState } from 'react'
import PropTypes from 'prop-types'
import Card from './Card'
import { items } from '../dummy_data/items'
import alcohol from '../assets/images/alcohol.jpg'
import bakery from '../assets/images/bakery.jpg'
import frozen from '../assets/images/frozen.jpg'
import fruits from '../assets/images/fruits.jpg'
import meat from '../assets/images/meat.jpg'
import milk from '../assets/images/milk.jpg'
import toilet from '../assets/images/toilet.jpg'
import ready_made_food from '../assets/images/ready_made_food.jpg'
import soft_drinks from '../assets/images/soft_drinks.jpg'

const images = [
  alcohol,
  bakery,
  frozen,
  fruits,
  meat,
  milk,
  toilet,
  ready_made_food,
  soft_drinks,
]

const Cards = (props) => {
  const { addItemToCart, removeItemFromCart } = props
  const cardItems = props.data.map((item, index) => (
    <Card
      key={item.id}
      item={item}
      image={item.image}
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
