import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import Request from './Request'
import Layout from './Layout'
import '../assets/styles/request.scss'

const Requests = (props) => {
  const requests = props.requests || []
  return (
    <Layout>
      {requests.length ? (
        <Request />
      ) : (
        <div>
          <p>You do not have a new request</p>
        </div>
      )}
      <div>
        <div>
          <p>Total request: {requests.length}</p>
        </div>
        {requests.map((request) => (
          <Request request={request} date={new Date()} />
        ))}
      </div>
    </Layout>
  )
}

Requests.propTypes = {}

export default Requests
