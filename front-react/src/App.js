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
import { requests } from './dummy_data/requests'

import CartCard from './components/CartCard'
import PrivateRoute from './components/shared/PrivateRoute'
import { getAccessToken } from './utils/cookies'
import CartCards from './components/CartCards'
import { getRandomImage } from './utils/get-random-image'
import Requests from './components/Requests'
import { useFetch } from './services/useFetch'
import AddItem from './components/AddItem'
import Register from './components/auth/Register'

const accessToken = getAccessToken()

const App = (props) => {
  const [data, setData] = useState([])
  const [cart, setCart] = useState([])
  const [requestData, setRequests] = useState(requests)
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

  const clearCart = () => {
    setCart([])
  }

  const fetchData = async () => {
    const url = 'http://localhost:5000/items/findByShopAndCategory'
    const response = await axios.get(url)

    const data = response.data.map((item) => {
      item.image = getRandomImage()
      return item
    })
    setData(data)
    // setRequests()
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
              clearCart={clearCart}
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
