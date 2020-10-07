import React from 'react'
import PropTypes from 'prop-types'
import Navbar from './Navbar'
import Footer from './Footer'

const Layout = (props) => {
  return (
    <div>
      <Navbar />
      {props.title && (
        <div>
          <h1>{props.title}</h1>
        </div>
      )}
      <div>{props.children}</div>
      <Footer />
    </div>
  )
}

Layout.propTypes = {}

export default Layout
