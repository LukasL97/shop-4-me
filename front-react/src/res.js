import React, { useState } from 'react'
import PropTypes from 'prop-types'
import Card from './Card'
import { items } from '../dummy_data/items'
import alcohol from '../assets/images/alcohol.jpg'
import bakery from '../assets/images/bakery.jpg'
import frozen from '../assets/images/frozen.jpg'
import fruits from '../assets/images/fruits.jpg'
import meat from '../assets/images/meat.jpg'
import milk from '../assets/images/milk.jpg'
import toilet from '../assets/images/toilet.jpg'
import ready_made_food from '../assets/images/ready_made_food.jpg'
import soft_drinks from '../assets/images/soft_drinks.jpg'

const images = [
  alcohol,
  bakery,
  frozen,
  fruits,
  meat,
  milk,
  toilet,
  ready_made_food,
  soft_drinks,
]

const Cards = (props) => {
  const [cart, setCart] = useState([])
  const addItemToCart = () => {
    alert('adding item to cart')
  }
  const removeItemFromCart = () => {
    alert('Removing item from cart')
  }
  const cardItems = props.data.map((item) => (
    <Card
      key={item.id}
      item={item}
      image={item.image}
      id={item.id}
      addItemToCart={addItemToCart}
      removeItemFromCart={removeItemFromCart}
    />
  ))
  return <div className='cards'>{cardItems}</div>
}

Cards.propTypes = {}

export default Cards

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
        <button onClick={addItemToCart} style={buttonStyles}>
          +
        </button>
        <button onClick={removeItemFromCart} style={buttonStyles}>
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
          <small>{price / 100}</small>
        </div>
      </div>
    </div>
  )
}

Card.propTypes = {}

export default Card
import React from 'react'
import { NavLink } from 'react-router-dom'
import SelectListGroup from '../shared/SelectListGroup'
import TextInputField from '../shared/TextInputField'
import PropTypes from 'prop-types'
import Layout from '../Layout'
import '../../assets/styles/form.scss'

const options = [
  {
    label: 'Select',
    value: '----',
  },
  {
    label: 'Requester',
    value: 'Requester',
  },
  {
    label: 'Volunteer',
    value: 'Volunteer',
  },
  {
    label: 'Shop Owner',
    value: 'Shop Owner',
  },
]

const Register = (props) => {
  return (
    <Layout>
      <form>
        <h1>Create your shop4me account by registering</h1>
        <SelectListGroup options={options} />
        <div className='form-group'>
          <TextInputField
            name='firstname'
            label='First name'
            type='text'
            placeholder='Firsty'
            required
          />
        </div>
        <TextInputField
          name='lastname'
          label='Last name'
          type='text'
          placeholder='Lastnamersson'
          required
        />
        <TextInputField
          name='email'
          label='Email'
          type='email'
          placeholder='e.g. email@provider.com'
          iconl='fa-envelope'
          inputCheck={(email) => {
            return email
              ? {
                  ok_message: 'This username is available',
                  iconr: 'fa-check',
                }
              : {
                  ok_message: null,
                  iconr: null,
                }
          }}
          required
        />
        <TextInputField
          name='password'
          label='Password'
          type='password'
          placeholder='e.g. something614SortaSecure'
          iconl='fa-user'
          inputCheck={(password) => {
            return password.length < 7
              ? {
                  ok_message: null,
                  error_message: 'Password is too short!',
                  iconr: null,
                }
              : {
                  ok_message: ' ',
                  error_message: null,
                  iconr: 'fa-check',
                }
          }}
          required
        />
        <TextInputField
          name='address'
          label='Street address'
          type='text'
          placeholder='e.g. Kyläsaarenkuja 5 B'
          required
        />
        <TextInputField
          name='zip'
          label='ZIP Code'
          type='number'
          placeholder='e.g. 00220'
          required
        />
        <div className='field'>
          <div className='control'>
            <label className='checkbox'>
              <input type='checkbox' /> I agree to the{' '}
              <a href='#'>terms and conditions</a>
            </label>
          </div>
        </div>
        <div className='field'>
          <div className='control'>
            <button className='button is-link' type='submit'>
              Register
            </button>{' '}
            <NavLink className='button is-link' to='/login'>
              Login
            </NavLink>
          </div>
        </div>
      </form>
    </Layout>
  )
}

Register.propTypes = {}

export default Register
