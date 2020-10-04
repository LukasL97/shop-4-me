import React, { Component } from 'react'
import Login from './Login'
import { BrowserRouter as Router, Route, Link, Switch } from 'react-router-dom'
import Navbar from './components/Navbar'
import Cards from './components/Cards'

// var ReactRouter = require('react-router-dom');
// var Router = ReactRouter.BrowserRouter;
// var Route = ReactRouter.Route;
// var Switch = ReactRouter.Switch;
// var Link = require('react-router-dom').Link;

class App extends Component {
  render() {
    return (
      <Router>
        <div className='container'>
          {/* <Navbar /> */}
          <Switch>
            <Route exact path='/login' component={Login} />
            <Route exact path='/' component={Home} />
            <Route render={() => <p>Not found</p>} />
          </Switch>
          <Footer />
        </div>
      </Router>
    )
  }
}

class Home extends Component {
  render() {
    return (
      <div className='home'>
        {/* <h1 className='home-header'>Shop-4-me</h1> */}
        <Navbar />
        <Cards />
        <div className='cards'>
          <div className='card'>
            <p>Card #1</p>
          </div>
          <div className='card'>
            <p>Card #2</p>
          </div>
          <div className='card'>
            <p>Card #3</p>
          </div>
        </div>
      </div>
    )
  }
}

function Footer(props) {
  return (
    <footer>&copy; 2020 -- Asabeneh, Lukas and Walter</footer>
  )
}

export default App
