import React from 'react'
import PropTypes from 'prop-types'

const Card = ({ item: { name, price }, image }) => {
  return (
    <div className='card'>
      <div className='card-image'>
        <img src={image} alt='' />
      </div>
      <h2>{name}</h2>
      <div>
        <small>{price/100}</small>
      </div>
      <div className='icons'>
        <i class='fas fa-thumbs-up'></i>
        <i class='fas fa-thumbs-down'></i>
        <i class='fas fa-star'></i>
      </div>
    </div>
  )
}

Card.propTypes = {}

export default Card
