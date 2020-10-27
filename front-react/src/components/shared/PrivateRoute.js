import React from 'react'
import { Route, Redirect } from 'react-router-dom'
import PropTypes from 'prop-types'


const PrivateRoute = ({ component: Component, accessToken, ...rest }) => (
  <Route
    {...rest}
    render={(props) =>
      accessToken === true ? <Component {...props} /> : <Redirect to='/login' />
    }
  />
)

export default PrivateRoute
