import React, { useState, useEffect } from 'react'
import { Route, Redirect } from 'react-router-dom'
import PropTypes from 'prop-types'
import { getAccessToken, deleteCookie } from '../../utils/cookies'
import Cookies from 'universal-cookie'

const PrivateRoute = ({ component: Component, onlyFor, ...rest }) => {
  const accessToken = getAccessToken()
  return (
    <Route
      {...rest}
      render={(props) =>
        accessToken && (!onlyFor || new Cookies().get('user_type') == onlyFor) ? <Component {...props} /> : <Redirect to='/login' />
      }
    />
  )
}

export default PrivateRoute
