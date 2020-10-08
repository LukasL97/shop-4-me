import React, { Component } from 'react'
import Login from './Login'
import { BrowserRouter as Router, Route, Link, Switch } from 'react-router-dom'
import Navbar from './components/Navbar'
import Cards from './components/Cards'
import About from './components/About'

class App extends Component {
  render() {
    return (
      <Router>
        <div className='container'>
          {/* <Navbar /> */}
          <Switch>
            <Route exact path='/login' component={Login} />
            <Route exact path='/about' component={About} />
            <Route exact path='/' component={Home} />
            <Route render={() => <p>Not found</p>} />
          </Switch>
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
      </div>
    )
  }
}



export default App
