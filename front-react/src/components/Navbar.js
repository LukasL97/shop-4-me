import React from 'react'
import { Link, NavLink } from 'react-router-dom'
import PropTypes from 'prop-types'
import '../assets/styles/navbar.scss'

const Navbar = (props) => {
  return (
    <div className='menu'>
      <div className='logo'>
        <a href='/' className='brand-name'>
          Shop4Me
        </a>

        <small>Bring the store to your door</small>
      </div>
      <ul>
        <li>
          <NavLink exact activeClassName='active' to='/'>
            Home
          </NavLink>
        </li>
        <li>
          <NavLink exact activeClassName='active' to='/about'>
            About
          </NavLink>
        </li>
        <li>
          <NavLink exact activeClassName='active' to='/shop-now'>
            Eligible
          </NavLink>
        </li>

        <li>
          <NavLink exact activeClassName='active' to='/shop-now'>
            Shop Now
          </NavLink>
        </li>

        <li>
          <NavLink exact activeClassName='active' to='/login'>
            Login
          </NavLink>
        </li>
      </ul>
    </div>
  )
}

Navbar.propTypes = {}

export default Navbar
