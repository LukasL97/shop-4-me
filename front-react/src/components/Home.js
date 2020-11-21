import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import Layout from './Layout'
import Cards from './Cards'
import Cookies from 'universal-cookie'
import AvailabilityCalendar from './Calendar'
import TextInputField from './shared/TextInputField'

const Home = ({
  data,
  addItemToCart,
  removeItemFromCart,
  filterProducts,
  notFound,
}) => {
  const [value, setValue] = useState('')
  const onChange = (e) => {
    e.preventDefault()
    setValue(e.target.value)
  }

  const onSubmit = (e) => {
    e.preventDefault()
    filterProducts(value)
  }

  const cookies = new Cookies()
  let userType = cookies.get('user_type')
  let renderContent =
    userType === 'Requester' ? (
      <Cards
        data={data}
        addItemToCart={addItemToCart}
        removeItemFromCart={removeItemFromCart}
      />
    ) : userType === 'Volunteer' ? (
      <AvailabilityCalendar />
    ) : (
      <Cards
        data={data}
        addItemToCart={addItemToCart}
        removeItemFromCart={removeItemFromCart}
      />
    )

  return (
    <Layout>
      <div className='search'>
        <form onSubmit={onSubmit}>
          <TextInputField
            name='search'
            value={value}
            onChange={onChange}
            autoFocus
            placeholder='Search products by name, category, description ..'
          />
          <button className='btn'>Search</button>
        </form>
      </div>
      {notFound ? <p>{notFound}</p> : renderContent}
    </Layout>
  )
}

Home.propTypes = {}

export default Home
