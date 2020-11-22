import React from 'react'
import PropTypes from 'prop-types'
import Layout from './Layout'

const CardDetail = (props) => {
  const id = props.match.params.id
  console.log(props)
  const {
    name,
    image,
    price,
    image: { url },
    details: { description },
  } = props.data.find((item) => item.id == id)

  if (!name) {
    return <h1>Loading...</h1>
  }

  return (
    <Layout>
      <div className='card'>
        <div className='card-image'>
          <img src={url} alt='' />
        </div>
        <div>
          <h2>{name}</h2>
        </div>
        <div>
          <p>{description}</p>
        </div>

        <div className='card-footer'>
          <div className='icons show'>
            <i className='fas fa-thumbs-up'></i>
            <i className='fas fa-thumbs-down'></i>
            <i className='fas fa-star'></i>
          </div>
          <div>
            <small>{price}</small>
          </div>
        </div>
      </div>
    </Layout>
  )
}

CardDetail.propTypes = {}

export default CardDetail
