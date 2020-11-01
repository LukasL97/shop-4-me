import React from 'react'
import PropTypes from 'prop-types'
import Layout from './Layout'
import Cards from './Cards'

const Home = ({ data, addItemToCart, removeItemFromCart }) => {
  return (
    <Layout>
      <Cards
        data={data}
        addItemToCart={addItemToCart}
        removeItemFromCart={removeItemFromCart}
      />
    </Layout>
  )
}

Home.propTypes = {}

export default Home
