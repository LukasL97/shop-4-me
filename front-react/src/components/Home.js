import React from 'react'
import PropTypes from 'prop-types'
import Layout from './Layout'
import Cards from './Cards'
import Cookies from 'universal-cookie'
import AvailabilityCalendar from './Calendar'

const Home = (props) => {
  const cookies = new Cookies();
  let userType = cookies.get('user_type');
  let component = userType === "Requester" ?
	<Cards data={props.data} addItemToCart={props.addItemToCart} /> :
	userType === "Volunteer" ?
    <AvailabilityCalendar /> :
	<Cards data={props.data} addItemToCart={props.addItemToCart} />
  
  return (
    <Layout>
      {component}
    </Layout>
  )
}

Home.propTypes = {}

export default Home
