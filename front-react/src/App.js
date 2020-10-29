import React, { Component, useState, useEffect } from 'react'
import axios from 'axios'
import Login from './Login'
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
import { parseCookies } from './utils/cookies'
import CartCards from './components/CartCards'
import { getRandomImage } from './utils/get-random-image'

const accessToken = parseCookies().access_token

const App = (props) => {
  const [data, setData] = useState([])
  const [cart, setCart] = useState(items)
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
    const url = 'http://localhost:5000/items/findByShopAndCategory'
    const response = await axios.get(url)

    const data = response.data.map((item) => {
      item.image = getRandomImage()
      return item
    })
    setData(data)
  }

  return (
    <Router>
      <Switch>
        <Route exact path='/login' component={Login} />
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
