import React from 'react'
import PropTypes from 'prop-types'
import { NavLink } from 'react-router-dom'

const Button = ({ onClick, text, styles }) => {
  return (
    <NavLink to='/login' onClick={onClick} style={{ color: 'red' }}>
      {text}
    </NavLink>
  )
}

Button.propTypes = {}

export default Button
