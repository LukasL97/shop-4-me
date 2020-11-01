import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Link, NavLink, Redirect } from 'react-router-dom'
import PropTypes from 'prop-types'
import '../assets/styles/navbar.scss'
import Button from './Button'
import { parseCookies, deleteCookie } from '../utils/cookies'

const Navbar = (props) => {
  const [auth, setAuth] = useState('')

  useEffect(() => {
    const accessToken = parseCookies().access_token
    setAuth(accessToken)
  }, [auth])

  const handleLogout = async () => {
    const url = 'http://localhost:5000/logout'
    // await axios.delete(url)
    deleteCookie()
    return <Redirect to='/login' />
  }
  console.log(auth)

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
        {auth && (
          <li>
            <NavLink exact activeClassName='active' to='/cart'>
              <i className='fas fa-shopping-cart'></i>
              {props.cart && <sup>123</sup>}
            </NavLink>
          </li>
        )}
        {!auth && (
          <li>
            <NavLink exact activeClassName='active' to='/login'>
              Login
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
