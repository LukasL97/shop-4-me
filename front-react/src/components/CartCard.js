import React from 'react'
import PropTypes from 'prop-types'
const buttonStyles = {
  padding: '10px 15px',
  cursor: 'pointer',
  margin: 3,
}

const CartCard = (props) => {
  return (
    <div className='cart-card'>
      <div className='cart-card-image'>
        <img src={props.item.image.url} alt='' />
      </div>
      <div style={{'margin-left': '300px'}}>
        <p> {props.item.name}</p>
        <small>Price: {props.item.price} euro</small>
      </div>

      <div style={{'margin-left': '300px'}}>
        <button
          onClick={() => props.removeItemFromCart(props.index)}
          style={buttonStyles}
        >
          -
        </button>
      </div>
    </div>
  )
}

CartCard.propTypes = {}

export default CartCard
