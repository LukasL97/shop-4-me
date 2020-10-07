import React from 'react'
import PropTypes from 'prop-types'
import Layout from './Layout'
import Cards from './Cards'

const Home = (props) => {
  return (
    <Layout>
      <Cards />
    </Layout>
  )
}

Home.propTypes = {}

export default Home
