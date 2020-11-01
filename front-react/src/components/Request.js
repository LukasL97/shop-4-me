import React from 'react'
import PropTypes from 'prop-types'
import moment from 'moment'

const Request = (props) => {
  console.log(props.request)
  if (props.request === undefined) {
    return <div>{/* <p>{props.request.id}</p> */}</div>
  } else {
    const {
      date,
      request: {
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
        </details>
      </div>
    )
  }
}

Request.propTypes = {}

export default Request
