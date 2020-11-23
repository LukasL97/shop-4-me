import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Link, NavLink, Redirect } from 'react-router-dom'
import PropTypes from 'prop-types'
import '../assets/styles/navbar.scss'
import Button from './Button'
import { getAccessToken, deleteCookie } from '../utils/cookies'
import Cookies from 'universal-cookie'

const Navbar = (props) => {
  const [auth, setAuth] = useState('')
  const [cart, setCart] = useState([])

  useEffect(() => {
    const accessToken = getAccessToken()
    setAuth(accessToken)
    let parsedCart = JSON.parse(localStorage.getItem('cart'))
    setCart(parsedCart)
  }, [auth])

  const handleLogout = async () => {
    const url = 'http://localhost:5000/logout'
    // await axios.delete(url)
    deleteCookie()
    return <Redirect to='/login' />
  }

  const is_SO = new Cookies().get('user_type') === 'ShopOwner'

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
        {auth && (
          <li>
            <NavLink exact activeClassName='active' to='/add-product'>
              Add Product
            </NavLink>
          </li>
        )}
        {is_SO && auth && (
          <li>
            <NavLink exact activeClassName='active' to='/add-shop'>
              Add Shop
            </NavLink>
          </li>
        )}
        {auth && (
          <li>
            <NavLink exact activeClassName='active' to='/requests'>
              Requests
            </NavLink>
          </li>
        )}

        {auth && (
          <li>
            <NavLink exact activeClassName='active' to='/carts'>
              <i className='fas fa-shopping-cart'></i>
              {cart && cart.length > 0 && <sup>{cart.length}</sup>}
            </NavLink>
          </li>
        )}
        {!auth && (
          <li>
            <NavLink exact activeClassName='active' to='/register'>
              Register
            </NavLink>
          </li>
        )}

        {auth && (
          <li>
            <Button text='Logout' onClick={handleLogout} />
          </li>
        )}
      </ul>
    </div>
  )
}

Navbar.propTypes = {}

export default Navbar
