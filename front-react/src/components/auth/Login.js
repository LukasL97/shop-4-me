import axios from 'axios'
import { NavLink } from 'react-router-dom'
import SelectListGroup from '../shared/SelectListGroup'
import TextInputField from '../shared/TextInputField'
import React, { useState } from 'react'
import Cookies from 'universal-cookie'
import Layout from '../../components/Layout'
import { getAccessToken } from '../../utils/cookies'

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
    value: 'ShopOwner',
  },
]

const Login = (props) => {
  const [formData, setFormData] = useState({
    userType: 'Requester',
    loginName: '',
    password: '',
  })
  const onChange = (e) => {
    const { name, value } = e.target
    setFormData({ ...formData, [name]: value })
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
    try {
      await axios.post('http://localhost:5000/login', formData).then(callback)
      const token = getAccessToken()
      if (token) {
        props.history.push('/')
      }
    } catch (error) {
      console.log(error)
    }
  }

  return (
    <Layout>
      <div className='login'>
        <form onSubmit={onSubmit}>
          <div className='row'>
            <h1 className='title'>
              Welcome to <strong>Shop-4-Me</strong>
            </h1>
            <h2 className='title'>Friendly neighborhood shopping assistant</h2>
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
          </div>

          <div className='row'>
            <div className='columns'>
              <div className='column is-one-fifth'>
                <TextInputField
                  name='loginName'
                  label='Email'
                  onChange={onChange}
                  value={formData.email}
                  type='email'
                  placeholder='e.g. email@provider.com'
                  required
                />
              </div>
              <div className='column is-one-fifth'>
                <TextInputField
                  name='password'
                  label='Password'
                  type='password'
                  onChange={onChange}
                  value={formData.password}
                  placeholder='e.g. iSecretlyLove50Cent'
                  required
                />
              </div>
            </div>
          </div>
          <div className='row'>
            <div className='column'>
              <button className='button is-link' type='submit'>
                Login
              </button>{' '}
              {}
              <NavLink className='button is-link' to='/register'>
                Register
              </NavLink>
            </div>
          </div>
        </form>
      </div>
    </Layout>
  )
}

export default Login
