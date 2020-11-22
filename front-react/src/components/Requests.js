import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import Request from './Request'
import Layout from './Layout'
import '../assets/styles/request.scss'

const Requests = (props) => {
  const own_requests = props.requests.own || []
  const open_requests = props.requests.open || []
  const OpenRequests = open_requests.length ? (
    <>
    <h2>Open requests</h2>
    <div>
      {open_requests.map((request) => (
        <Request request={request} date={new Date()} />
      ))}
    </div>
    </>
  ) : <></>
  return (
    <Layout>
      <h2>Pending requests</h2>
      {own_requests.length ? (
        <div>
          {own_requests.map((request) => (
            <Request request={request} date={new Date()} />
          ))}
        </div>
      ) : (
        <div>
          <p>You do not have pending requests</p>
        </div>
      )}
	  {OpenRequests}
    </Layout>
  )
}

Requests.propTypes = {}

export default Requests
