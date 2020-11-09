import React from 'react'
import PropTypes from 'prop-types'
import moment from 'moment'
import axios from 'axios'
import Cookies from 'universal-cookie'

async function accept(event, requestId) {
  const cookies = new Cookies()
  
  let data = {
    request: requestId,
    sessionId: cookies.get('access_token')
  }
  await axios.patch('http://localhost:5000/request/accept', data).then((response) => {
    //redirect somewhere
  })
}

const Request = (props) => {
  console.log(props.request)
  if (props.request === undefined) {
    return <div>{/* <p>{props.request.id}</p> */}</div>
  } else {
    const {
      date,
      request: {
        id,
        requester,
        items,
        deliveryAddress: {
          streetName,
          zip,
          coordinates: { lat, lng },
        },
      },
    } = props
    const itemList = items.map((item) => <li>{item.name}</li>)
    const totalPrice = items.reduce((acc, cur) => acc + Number(cur.amount), 0)

    return (
      <div className='request-card'>
        <details>
          <summary className='request-summary'>
            <span className='date'>
              {' '}
              {moment(date).format('DD/MM/YYYY HH:mm A')}{' '}
            </span>
            <span className=''> Requested by {requester}</span>
            <span className='total-price'>{totalPrice} EURO</span>
          </summary>
          <div>
            <p>Street Name: {streetName}</p>
            <p>Zipcode: {zip}</p>
            <p>
              {' '}
              Coordinates:({lat},{lng})
            </p>
            <div>
              <p>Items</p>
              <ul>{itemList}</ul>
            </div>
          </div>
          {
          new Cookies().get('user_type') == 'Volunteer' ?
            <button className='button is-link' onClick={(event) => accept(event, id)}> Accept </button> :
            <div></div>
          }
        </details>
      </div>
    )
  }
}

Request.propTypes = {}

export default Request
