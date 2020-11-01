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
  const [cart, setCart] = useState([])
  const addItemToCart = () => {
    alert('adding item to cart')
  }
  const removeItemFromCart = () => {
    alert('Removing item from cart')
  }
  const cardItems = props.data.map((item) => (
    <Card
      key={item.id}
      item={item}
      image={item.image}
      id={item.id}
      addItemToCart={addItemToCart}
      removeItemFromCart={removeItemFromCart}
    />
  ))
  return <div className='cards'>{cardItems}</div>
}

Cards.propTypes = {}

export default Cards

import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import PropTypes from 'prop-types'

const buttonStyles = {
  padding: '10px 15px',
  cursor: 'pointer',
  margin: 3,
}

const Card = ({
  item: { name, price, id },
  image,
  addItemToCart,
  removeItemFromCart,
}) => {
  const [visibility, setVisibility] = useState(false)
  return (
    <div className='card'>
      <Link to={`/card/${id}`}>
        <div className='card-image'>
          <img src={image} alt='' />
        </div>
        <div>
          <h2>{name}</h2>
        </div>
      </Link>
      <div>
        <button onClick={addItemToCart} style={buttonStyles}>
          +
        </button>
        <button onClick={removeItemFromCart} style={buttonStyles}>
          -
        </button>
      </div>
      <div className='card-footer'>
        <div className='icons show'>
          <i class='fas fa-thumbs-up'></i>
          <i class='fas fa-thumbs-down'></i>
          <i class='fas fa-star'></i>
        </div>
        <div>
          <small>{price / 100}</small>
        </div>
      </div>
    </div>
  )
}

Card.propTypes = {}

export default Card
