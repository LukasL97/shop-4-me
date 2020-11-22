import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import Request from './Request'
import Layout from './Layout'
import Cookies from 'universal-cookie'
import '../assets/styles/request.scss'

const Requests = (props) => {
	const Component = new Cookies().get('user_type') == 'Volunteer' ? 
		<VolunteerRequests {...props}/> :
		<OtherRequests {...props}/>
	return <Layout>{Component}</Layout>
}

const SUBMITTED = 1;
const ACCEPTED = 2;

const OtherRequests = (props) => {
  const own_requests = props.requests.own || []
  const OwnRequests = own_requests.length ? (
    <>
    <h2>Pending requests</h2>
    <div>
      {own_requests.filter((req) => req.status === SUBMITTED).map((request) => (
        <Request request={request} />
      ))}
    </div>
    <h2>Closed requests</h2>
    <div>
      {own_requests.filter((req) => req.status === ACCEPTED).map((request) => (
        <Request request={request} />
      ))}
    </div>
    </>
  ) :
  <div>
	<p>You have not submitted any requests</p>
  </div>
  
  return OwnRequests
}

const VolunteerRequests = (props) => {
  const own_requests = props.requests.own || []
  const open_requests = props.requests.open || []
  const OpenRequests = open_requests.length ? (
    <>
    <h2>Open requests</h2>
    <div>
      {open_requests.filter((req) => req.status === 1).map((request) => (
        <Request request={request} />
      ))}
    </div>
    <h2>Closed requests</h2>
    <div>
      {open_requests.filter((req) => req.status === 2).map((request) => (
        <Request request={request} />
      ))}
    </div>
    </>
  ) : <></>
  
  return (
    <Layout>
      <h2>Accepted requests</h2>
      {own_requests.length ? (
        <div>
          {own_requests.map((request) => (
            <Request request={request} />
          ))}
        </div>
      ) : (
        <div>
          <p>You have not yet accepted any requests</p>
        </div>
      )}
	  {OpenRequests}
    </Layout>
  )
}

Requests.propTypes = {}

export default Requests
