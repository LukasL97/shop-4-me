import React from 'react'
import { Link, NavLink } from 'react-router-dom'
import PropTypes from 'prop-types'
import '../assets/styles/navbar.scss'
import Button from './Button'
import { parseCookies } from '../utils/cookies'

const Navbar = (props) => {
  const accessToken = parseCookies().accessToken
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
          <NavLink exact activeClassName='active' to='/eligible'>
            Eligible
          </NavLink>
        </li>
        <li>
          <NavLink exact activeClassName='active' to='/shop-now'>
            Shop Now
          </NavLink>
        </li>
        {accessToken && (
          <li>
            <NavLink exact activeClassName='active' to='/cart'>
              <i className='fas fa-shopping-cart'></i>
              {props.cart && <sup>123</sup>}
            </NavLink>
          </li>
        )}
        <li>
          <NavLink exact activeClassName='active' to='/login'>
            Login
          </NavLink>
        </li>
        {accessToken && (
          <li>
            <Button text='Logout' />
          </li>
        )}
      </ul>
    </div>
  )
}

Navbar.propTypes = {}

export default Navbar
