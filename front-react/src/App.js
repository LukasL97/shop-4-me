import React, { Component } from 'react'
import Login from './Login'
import { BrowserRouter as Router, Route, Link, Switch } from 'react-router-dom'
import Navbar from './components/Navbar'
import Cards from './components/Cards'
import About from './components/About'
import Home from './components/Home'
import NotFound from './components/NotFound'
import CardDetail from './components/CardDetail'
import { items } from './dummy_data/items'

import alcohol from './assets/images/alcohol.jpg'
import bakery from './assets/images/bakery.jpg'
import frozen from './assets/images/frozen.jpg'
import fruits from './assets/images/fruits.jpg'
import meat from './assets/images/meat.jpg'
import milk from './assets/images/milk.jpg'
import toilet from './assets/images/toilet.jpg'
import ready_made_food from './assets/images/ready_made_food.jpg'
import soft_drinks from './assets/images/soft_drinks.jpg'

const images = [
  alcohol,
  bakery,
  frozen,
  fruits,
  meat,
  milk,
  toilet,
  ready_made_food,
  soft_drinks,
]
const data = items.map((item) => {
  let randIndex = Math.floor(Math.random() * images.length)
  let image = images[randIndex]
  item.image = image
  return item
})

class App extends Component {
  state = {
    data: data,
  }
  render() {
    return (
      <Router>
        <Switch>
          <Route exact path='/login' component={Login} />
          <Route exact path='/about' component={About} />
          <Route
            exact
            path='/card/:id'
            component={(props) => (
              <CardDetail {...props} data={this.state.data} />
            )}
          />
          <Route
            exact
            path='/'
            component={() => <Home data={this.state.data} />}
          />
          <Route component={NotFound} />
        </Switch>
      </Router>
    )
  }
}

export default App
