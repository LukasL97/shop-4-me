import React from 'react'
import PropTypes from 'prop-types'
import Navbar from './Navbar'
import Footer from './Footer'
import Header from './Header'

const Layout = (props) => {
  return (
    <>
      <Header />
      {props.title && (
        <div>
          <h1>{props.title}</h1>
        </div>
      )}
      <main>
        <div className='main-wrapper'>{props.children}</div>
      </main>
      <Footer />
    </>
  )
}

Layout.propTypes = {}

export default Layout
