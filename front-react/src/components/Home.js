import React from 'react'
import PropTypes from 'prop-types'
import Layout from './Layout'
import Cards from './Cards'
import Cookies from 'universal-cookie'
import AvailabilityCalendar from './Calendar'

const Home = ({ data, addItemToCart, removeItemFromCart }) => {
  const cookies = new Cookies();
  let userType = cookies.get('user_type');
  let component = userType === "Requester" ?
	<Cards
		data={data}
		addItemToCart={addItemToCart}
		removeItemFromCart={removeItemFromCart}
	/>
	: userType === "Volunteer" ?
    <AvailabilityCalendar /> :
	<Cards
	  data={data}
	  addItemToCart={addItemToCart}
	  removeItemFromCart={removeItemFromCart}
	/>
  
  return (
    <Layout>
      {component}
    </Layout>
  )
}

Home.propTypes = {}

export default Home
