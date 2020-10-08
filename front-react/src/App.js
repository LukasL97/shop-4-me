import React, { Component } from 'react'
import Login from './Login'
import { BrowserRouter as Router, Route, Link, Switch } from 'react-router-dom'
import Navbar from './components/Navbar'
import Cards from './components/Cards'
import About from './components/About'
import Home from './components/Home'

class App extends Component {
  render() {
    return (
      <Router>
        <Switch>
          <Route exact path='/login' component={Login} />
          <Route exact path='/about' component={About} />
          <Route exact path='/' component={Home} />
          <Route render={() => <p>Not found</p>} />
        </Switch>
      </Router>
    )
  }
}

export default App
