import React, { useState, useEffect } from 'react'
import { Route, Redirect } from 'react-router-dom'
import PropTypes from 'prop-types'
import { parseCookies, deleteCookie } from '../../utils/cookies'
console.log(parseCookies().access_token)

const PrivateRoute = ({ component: Component, ...rest }) => {
  const accessToken = parseCookies().access_token
  return (
    <Route
      {...rest}
      render={(props) =>
        accessToken ? <Component {...props} /> : <Redirect to='/login' />
      }
    />
  )
}

export default PrivateRoute
