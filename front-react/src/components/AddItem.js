import React, { useState } from 'react'
import axios from 'axios'
import PropTypes from 'prop-types'
import TextInputField from './shared/TextInputField'
import TextAreaField from './shared/TextAreaField'
import Layout from './Layout'
import '../assets/styles/add-item.scss'
import '../assets/styles/buttons.scss'
import '../assets/styles/input-file.scss'

const AddItem = (props) => {
  const initialState = {
    name: '',
    price: '',
    category: '',
    description: '',
    image: '',
    fileUrl: '',
  }
  const [errors, setErrors] = useState({})
  const [formData, setFormData] = useState(initialState)
  const onChange = (e) => {
    const { name, type, value } = e.target
    setFormData({ ...formData, [name]: value })

    if (type === 'file') {
      const files = e.target.files
      setFormData({
        ...formData,
        image: files[0],
        fileUrl: URL.createObjectURL(files[0]),
      })
    }
  }

  const onSubmit = (e) => {
    e.preventDefault()
    console.log(formData)
    const url = ''
    const config = {
      Accept: 'application/json',
      headers: { 'Content-Type': 'multipart/form-data' },
    }
    const data = new FormData()
    for (const key in formData) {
      data.append(key, formData[key])
    }

    axios({
      method: 'post',
      url: url,
      data,
    })
      .then((response) => {
        props.fetchData()
        props.history.push('/items')
      })
      .catch((err) => {
        setErrors(err.response.data)
      })
  }

  const { name, category, description, price } = errors

  return (
    <Layout>
      <div className='add-item-container'>
        <form onSubmit={onSubmit} noValidate>
          <div className='row'>
            <TextInputField
              label=''
              id='name'
              type='text'
              name='name'
              value={formData.name}
              onChange={onChange}
              placeholder='Product Name'
              error={name}
            />
            <TextInputField
              label=''
              id='price'
              type='text'
              name='price'
              value={formData.price}
              onChange={onChange}
              placeholder='Price'
              error={price}
            />
            <TextInputField
              label=''
              id='category'
              type='text'
              name='category'
              value={formData.category}
              onChange={onChange}
              placeholder='Category'
              error={category}
            />
          </div>

          <TextAreaField
            label=''
            id='description'
            name='description'
            cols='120'
            rows='15'
            value={formData.description}
            onChange={onChange}
            placeholder='Product description  goes here ...'
            error={description}
          />
          {formData.fileUrl && (
            <div>
              <img src={formData.fileUrl} alt='' />
            </div>
          )}

          <div className='form-group file-upload'>
            <input
              type='file'
              onChange={onChange}
              name='image'
              id='image'
              className={'inputfile'}
            />
            <label htmlFor='image'>
              <strong>
                <i class='far fa-image'></i>{' '}
                {formData.image.name ? formData.image.name : 'Upload a photo'}
              </strong>
            </label>
          </div>

          <button className='btn' type='submit' id='submit-button'>
            Add Product
          </button>
        </form>
      </div>
    </Layout>
  )
}

export default AddItem
