import React from 'react';
import Cookies from 'universal-cookie';

var ReactRouter = require('react-router-dom');

function Login() {
  let history = ReactRouter.useHistory()

  function handleSubmit(event) {
    event.preventDefault();
    // TODO POST to backend

    var callback = (data) => {
      const cookies = new Cookies();
      cookies.set('access_token', data.access_token, { path: '/', expires: data.expiry_time })
      cookies.set('refresh_token', data.refresh_token, { path: '/' })
    }
    callback({
      access_token: "blah",
      refresh_token: "blöh",
      expiry_time: new Date(new Date().getTime() + 60 * 60 * 1000)
    })

    history.push('/home')
  }

  return (
      <div className='login'>
        <h1>Welcome! Please log in</h1>
        <form onSubmit={handleSubmit}>
          <label for="username"><b>Username</b></label>
          <input type="text" placeholder="Enter Username" name="username" required></input>
          <br />
          <label for="password"><b>Password</b></label>
          <input type="password" placeholder="Enter Password" name="password" required></input>

          <button type="submit">Login</button>
        </form>
      </div>
    )
}

export default Login;