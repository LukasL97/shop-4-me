import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import PropTypes from 'prop-types'

const buttonStyles = {
  padding: '10px 15px',
  cursor: 'pointer',
  margin: 3,
}

const Card = ({
  item: {
    name,
    price,
    id,
    image,
    details: { description },
  },
  addItemToCart,
  removeItemFromCart,
  index,
}) => {
  const [visibility, setVisibility] = useState(false)
  let formattedPrice = price.toFixed(2)
  return (
    <div className='card'>
      <Link to={`/card/${id}`}>
        <div className='card-image'>
          <img src={image.url} alt='' />
        </div>
        <div>
          <h2>{name}</h2>
          <small className='product-description'>{description}</small>
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
          <i className='fas fa-thumbs-up'></i>
          <i className='fas fa-thumbs-down'></i>
          <i className='fas fa-star'></i>
        </div>
        <div>
          <small>{formattedPrice}</small>
        </div>
      </div>
    </div>
  )
}

Card.propTypes = {}

export default Card
