import React, { Component, useState, useEffect } from 'react'
import axios from 'axios'
// import Login from './Login'
import Login from './components/auth/Login'
import { BrowserRouter as Router, Route, Link, Switch } from 'react-router-dom'
import Navbar from './components/Navbar'
import Cards from './components/Cards'
import About from './components/About'
import Home from './components/Home'
import NotFound from './components/NotFound'
import CardDetail from './components/CardDetail'
import { items } from './dummy_data/items'

import CartCard from './components/CartCard'
import PrivateRoute from './components/shared/PrivateRoute'
import { getAccessToken } from './utils/cookies'
import CartCards from './components/CartCards'
import { getRandomImage } from './utils/get-random-image'
import Requests from './components/Requests'
import { useFetch } from './services/useFetch'
import AddItem from './components/AddItem'
import Register from './components/auth/Register'
import Cookies from 'universal-cookie'

const accessToken = getAccessToken()

const App = (props) => {
  const [data, setData] = useState([])
  const [cart, setCart] = useState([])
  const [requestData, setRequests] = useState([])
  useEffect(() => {
    fetchData()
    const cartStr = JSON.stringify(cart)
    localStorage.setItem('cart', cartStr)
  }, [cart])

  const addItemToCart = (item) => setCart([...cart, item])

  const removeItemFromCart = (index) => {
    const cartItems = [...cart]
    cartItems.splice(index, 1)
    setCart(cartItems)
  }

  const fetchData = async () => {
    let data = (await axios.get('http://localhost:5000/items/findByShopAndCategory')).data.map((item) => {
      item.image = getRandomImage()
      return item
    })
    setData(data)
    const cookies = new Cookies();
    let open_requests = cookies.get('user_type') == 'Volunteer' ?
      (await axios.post('http://localhost:5000/requests/open', {
        sessionId: cookies.get('access_token'),
        area: {
          range: 100,
          lat: 0,
          lng: 0
        }
      })).data : []
    let own_requests = (await axios.post('http://localhost:5000/requests/own', {
        userType: cookies.get('user_type'),
        sessionId: cookies.get('access_token')
    })).data
    setRequests(own_requests.push(...open_requests))
  }

  return (
    <Router>
      <Switch>
        <Route exact path='/login' component={Login} />
        <Route exact path='/register' component={Register} />
        <Route exact path='/about' component={About} />
        <Route
          exact
          path='/card/:id'
          component={(props) => <CardDetail {...props} data={data} />}
        />
        <PrivateRoute
          path='/carts'
          component={(props) => (
            <CartCards
              {...props}
              cart={cart}
              removeItemFromCart={removeItemFromCart}
            />
          )}
        />
        <PrivateRoute
          path='/cart'
          component={(props) => <CartCard {...props} cart={cart} />}
        />
        <PrivateRoute
          path='/requests'
          component={(props) => <Requests {...props} requests={requestData} />}
        />
        <PrivateRoute path='/add-product' component={(props) => <AddItem />} />

        <Route
          exact
          path='/'
          component={() => (
            <Home
              data={data}
              addItemToCart={addItemToCart}
              removeItemFromCart={removeItemFromCart}
            />
          )}
        />
        <Route component={NotFound} />
      </Switch>
    </Router>
  )
}

export default App
