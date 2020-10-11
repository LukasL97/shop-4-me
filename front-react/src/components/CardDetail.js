import React from 'react'
import PropTypes from 'prop-types'
import Layout from './Layout'

const CardDetail = (props) => {
  console.log(props)
  const id = props.match.params.id
  const { name, image, price } = props.data.find((item) => item.id == id)
  return (
    <Layout>
      <div className='card'>
        <div className='card-image'>
          <img src={image} alt='' />
        </div>
        <div>
          <h2>{name}</h2>
        </div>
        <div>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorum
            nesciunt maiores quas asperiores non itaque fuga nostrum molestiae
            voluptates corrupti modi, aliquid a nulla quia! Repellat quo fuga
            itaque corrupti.
          </p>
        </div>

        <div className='card-footer'>
          <div className='icons show'>
            <i class='fas fa-thumbs-up'></i>
            <i class='fas fa-thumbs-down'></i>
            <i class='fas fa-star'></i>
          </div>
          <div>
            <small>{price / 100}</small>
          </div>
        </div>
      </div>
    </Layout>
  )
}

CardDetail.propTypes = {}

export default CardDetail
