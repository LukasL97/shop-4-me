import React from 'react'
import PropTypes from 'prop-types'
import Navbar from './Navbar'

const Header = (props) => {
  return (
    <header>
      <div className='header-wrapper'>
        <Navbar />
        {props.title && <h3 className='page-title'>{props}</h3>}
      </div>
    </header>
  )
}

Header.propTypes = {}

export default Header
