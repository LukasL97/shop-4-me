import React, { useState } from 'react'
import { NavLink } from 'react-router-dom'
import SelectListGroup from '../shared/SelectListGroup'
import TextInputField from '../shared/TextInputField'
import PropTypes from 'prop-types'
import Layout from '../Layout'
import axios from 'axios'
import Cookies from 'universal-cookie'
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
    loginName: '',
    password: '',
    firstName: '',
    lastName: '',
    agreed: false,
    zip: '',
  }

  const [formData, setFormData] = useState(initialData)
  const onChange = (e) => {
    const { name, value, checked } = e.target
    setFormData({ ...formData, [name]: value, agree: checked })
  }
  const onSubmit = async (e) => {
    e.preventDefault()
    console.log(formData)
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
    try {
      await axios
        .post('http://localhost:5000/register', formData)
        .then(callback)
      props.history.push('/login')
    } catch (error) {
      console.log(error)
    }
  }

  console.log(formData)
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
                inputCheck={(email) => {
                  return email
                    ? {
                        ok_message: 'This username is available',
                        iconr: 'fa-check',
                      }
                    : {
                        ok_message: null,
                        iconr: null,
                      }
                }}
                required
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
                inputCheck={(password) => {
                  return password.length < 7
                    ? {
                        ok_message: null,
                        error_message: 'Password is too short!',
                        iconr: null,
                      }
                    : {
                        ok_message: ' ',
                        error_message: null,
                        iconr: 'fa-check',
                      }
                }}
                required
              />
            </div>
          </div>
        </div>
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
                required
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
                required
              />
            </div>
          </div>
        </div>
        <div className='row'>
          <div className='column'>
            <div className='field'>
              <div className='control'>
                <label className='checkbox'>
                  <TextInputField
                    type='checkbox'
                    onChange={onChange}
                    name='agreed'
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
