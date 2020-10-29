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
  index,
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
        <button
          onClick={() => addItemToCart({ name, price, id, image })}
          style={buttonStyles}
        >
          +
        </button>
        <button onClick={() => removeItemFromCart(index)} style={buttonStyles}>
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
          <small>{price /10}</small>
        </div>
      </div>
    </div>
  )
}

Card.propTypes = {}

export default Card
