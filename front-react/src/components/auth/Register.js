import React, { useState } from 'react'
import { NavLink } from 'react-router-dom'
import SelectListGroup from '../shared/SelectListGroup'
import TextInputField from '../shared/TextInputField'
import PropTypes from 'prop-types'
import Layout from '../Layout'
import axios from 'axios'
import Cookies from 'universal-cookie'
import validator from 'validator'

const options = [
  {
    label: 'Requester',
    value: 'Requester',
  },
  {
    label: 'Volunteer',
    value: 'Volunteer',
  },
  {
    label: 'Shop Owner',
    value: 'Shop Owner',
  },
]

const Register = (props) => {
  const initialData = {
    userType: 'Requester',
    firstName: '',
    lastName: '',
    password: '',
    address: '',
    zip: '',
    agreed: false,
    touched: {
      firstName: false,
      lastName: false,
      address: false,
      zip: false,
      agreed: false,
    },
  }

  const [formData, setFormData] = useState(initialData)
  const onChange = (e) => {
    const { name, value, checked } = e.target
    setFormData({ ...formData, [name]: value, agree: checked })
  }
  const onBlur = (e) => {
    const { name } = e.target
    setFormData({ ...formData, touched: { ...formData.touched, [name]: true } })
  }
  const validate = () => {
    const errors = {
      firstName: '',
      lastName: '',
      address: '',
      zip: '',
    }

    // first
    if (
      formData.touched.firstName &&
      !validator.isLength(formData.firstName, {
        min: 2,
        max: 12,
      })
    ) {
      errors.firstName = 'First name should be between 2 and 12 characters'
    }

    if (formData.touched.firstName && validator.isEmpty(formData.firstName)) {
      errors.firstName = 'Last name is required'
    }

    // last name
    if (
      formData.touched.lastName &&
      !validator.isLength(formData.lastName, {
        min: 2,
        max: 12,
      })
    ) {
      errors.lastName = 'Last name should be between 2 and 12 characters'
    }

    if (formData.touched.lastName && validator.isEmpty(formData.lastName)) {
      errors.lastName = 'Last name is required'
    }

    // Email

    if (formData.touched.email && !validator.isEmail(formData.email)) {
      errors.email = 'It must be a valid email'
    }
    if (formData.touched.email && validator.isEmpty(formData.email)) {
      errors.email = 'Email is required'
    }

    if (formData.touched.password && validator.isEmpty(formData.password)) {
      errors.password = 'Password is required'
    }

    if (
      formData.touched.password &&
      !validator.isLength(formData.password, { min: 6, max: 30 })
    ) {
      errors.password = 'Password must be between 6 to 30 characters'
    }
    if (formData.touched.password && validator.isEmpty(formData.password)) {
      errors.password = 'Password is required'
    }
    if (
      formData.touched.address &&
      !validator.isLength(formData.address, {
        min: 2,
        max: 30,
      })
    ) {
      errors.address = 'Address should be between 3 to 30 characters'
    }
    if (formData.touched.address && validator.isEmpty(formData.address)) {
      errors.address = 'Address is required'
    }
    if (
      formData.touched.zip &&
      !validator.isLength(formData.zip, {
        min: 2,
        max: 10,
      })
    ) {
      errors.zip = 'Zip should be between 3 to 10 characters'
    }

    if (formData.touched.zip && validator.isEmpty(formData.zip)) {
      errors.zip = 'Zip is required'
    }

    return errors
  }

  const onSubmit = async (e) => {
    e.preventDefault()
    const callback = (res) => {
      console.log(res)
      const cookies = new Cookies()
      cookies.set('access_token', res.data, {
        path: '/',
        expires: new Date(new Date().getTime() + 60 * 60 * 1000),
      })
      cookies.set('user_type', formData.userType, {
        path: '/',
        expires: new Date(new Date().getTime() + 60 * 60 * 1000),
      })
    }

    let data
    const loginName = formData.email

    if (formData.userType === 'Requester') {
      const {
        userType,
        firstName,
        lastName,
        email,
        password,
        agreed,
        address,
        zip,
      } = formData

      data = {
        userType,
        firstName,
        lastName,
        email,
        loginName,
        password,
        agreed,
        address,
        zip,
      }
    } else if (formData.value === 'Shop Owner') {
      data.userType = 'ShopOwner'
    } else {
      const {
        firstName,
        userType,
        lastName,
        email,
        password,
        agreed,
      } = formData
      data = {
        firstName,
        lastName,
        email,
        loginName,
        password,
        agreed,
        userType,
      }
    }

    try {
      await axios.post('http://localhost:5000/register', data).then(callback)
      props.history.push('/login')
    } catch (error) {
      console.log(error)
    }

    if (formData.agreed) {
    } else {
      // setFormData({...formData})
    }
  }

  const errors = validate()

  return (
    <Layout>
      <form onSubmit={onSubmit}>
        <div className='row'>
          <div className='columns'>
            <div className='column'>
              <SelectListGroup
                options={options}
                name='userType'
                value={formData.userType}
                onChange={onChange}
              />
            </div>
          </div>
          <div className='columns'>
            <div className='column is-one-quarter'>
              <TextInputField
                name='firstName'
                label='First name'
                value={formData.firstName}
                onChange={onChange}
                type='text'
                placeholder='First Name'
                onBlur={onBlur}
                error={errors.firstName}
              />
            </div>
            <div className='column is-one-quarter'>
              <TextInputField
                name='lastName'
                label='Last name'
                value={formData.lastName}
                onChange={onChange}
                type='text'
                placeholder='Last Name'
                onBlur={onBlur}
                error={errors.lastName}
              />
            </div>
          </div>
        </div>
        <div className='row'>
          <div className='columns'>
            <div className='column is-one-quarter'>
              <TextInputField
                name='email'
                label='Email'
                value={formData.email}
                onChange={onChange}
                type='email'
                placeholder='e.g. email@provider.com'
                iconl='fa-envelope'
                onBlur={onBlur}
                error={errors.email}
              />
            </div>
            <div className='column is-one-quarter'>
              <TextInputField
                name='password'
                label='Password'
                type='password'
                value={formData.password}
                onChange={onChange}
                placeholder='e.g. something614SortaSecure'
                iconl='fa-user'
                onBlur={onBlur}
                error={errors.password}
              />
            </div>
          </div>
        </div>
        {formData.userType === 'Requester' ? (
          <div className='row'>
            <div className='columns'>
              <div className='column is-one-quarter'>
                <TextInputField
                  name='address'
                  label='Street address'
                  value={formData.address}
                  onChange={onChange}
                  type='text'
                  placeholder='e.g. Kyläsaarenkuja 5 B'
                  onBlur={onBlur}
                  error={errors.address}
                />
              </div>
              <div className='column is-one-quarter'>
                <TextInputField
                  name='zip'
                  label='ZIP Code'
                  value={formData.zip}
                  onChange={onChange}
                  type='number'
                  placeholder='e.g. 00220'
                  onBlur={onBlur}
                  error={errors.zip}
                />
              </div>
            </div>
          </div>
        ) : (
          ''
        )}

        <div className='row'>
          <div className='column'>
            <div className='field'>
              <div className='control'>
                <label className='checkbox'>
                  <TextInputField
                    type='checkbox'
                    onChange={onChange}
                    name='agreed'
                    onBlur={onBlur}
                    error={errors.agreed}
                  />{' '}
                  I agree to the <a href='#'>terms and conditions</a>
                </label>
              </div>
            </div>
          </div>
        </div>
        <div className='row'>
          <div className='field'>
            <div className='control'>
              <button className='button is-link' type='submit'>
                Register
              </button>{' '}
              <NavLink className='button is-link' to='/login'>
                Login
              </NavLink>
            </div>
          </div>
        </div>
      </form>
    </Layout>
  )
}

Register.propTypes = {}

export default Register
