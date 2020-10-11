import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import PropTypes from 'prop-types'

const Card = ({ item: { name, price, id }, image }) => {
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
