import React, { Component } from 'react';

var ReactRouter = require('react-router-dom');
var Router = ReactRouter.BrowserRouter;
var Route = ReactRouter.Route;
var Switch = ReactRouter.Switch;
var Link = require('react-router-dom').Link;

class App extends Component {
  render() {
    return (
      <Router>
        <div className='container'>
          <Switch>
            <Route exact path='/' component={Home} />
            <Route render={
              function() {
                return <p>Not found</p>
              }
            } />
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
        <h1 className='home-header'>Shop-4-me</h1>
      </div>
    )
  }
}

function Footer(props) {
  return (
    <footer>&copy; 2020 </footer>
  )
}


export default App;

