import React from 'react'
import { Route, Redirect } from 'react-router-dom'
import PropTypes from 'prop-types'
import { parseCookies } from '../../utils/cookies'

const accessToken = parseCookies().access_token

const PrivateRoute = ({ component: Component, ...rest }) => (
  <Route
    {...rest}
    render={(props) =>
      accessToken === true ? <Component {...props} /> : <Redirect to='/login' />
    }
  />
)

export default PrivateRoute
