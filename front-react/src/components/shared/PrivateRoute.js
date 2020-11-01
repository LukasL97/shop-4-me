import React, { useState, useEffect } from 'react'
import { Route, Redirect } from 'react-router-dom'
import PropTypes from 'prop-types'
import { getAccessToken, deleteCookie } from '../../utils/cookies'

const PrivateRoute = ({ component: Component, ...rest }) => {
  const accessToken = getAccessToken()
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
