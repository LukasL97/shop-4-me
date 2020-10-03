import React from 'react';
import Cookies from 'universal-cookie';

var ReactRouter = require('react-router-dom');

function Login() {
    let history = ReactRouter.useHistory()

    return (
        <div className='login'>
            <h1>Welcome! Please log in</h1>
            <LoginUserTypeSelector />
            <LoginSignIn />
            <LoginRegister />
        </div>
    )
}

function LoginSignIn() {

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

        //history.push('/home')
    }

    return (
        <form onSubmit={handleSubmit}>
            <label for="username"><b>Username</b></label>
            <input type="text" placeholder="Enter Username" name="username" required></input>
            <br />
            <label for="password"><b>Password</b></label>
            <input type="password" placeholder="Enter Password" name="password" required></input>
            <br />
            <button type="submit">Login</button>
        </form>
    )
}

function LoginRegister() {

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

        //history.push('/home')
        //use <Redirect>
    }

    let component = RegisterRequester()

    return (
        <div>
            {component}
        </div>
    )

}

function RegisterShared() {
    return (
        <div>
            <label for="firstname"><b>First name</b></label>
            <input type="text" placeholder="Firsty" name="firstname" required></input>
            <br />
            <label for="lastname"><b>Last name</b></label>
            <input type="text" placeholder="Lastnamersson" name="lastname" required></input>
            <br />
            <label for="email"><b>Email</b></label>
            <input type="text" placeholder="email@provider.com" name="email" required></input>
            <br />
            <label for="password"><b>Password</b></label>
            <input type="password" placeholder="e.g. something614SortaSecure" name="password" required></input>
        </div>
    )
}

function AddressPart() {
    return (
        <div>
            <label for="address"><b>Street address</b></label>
            <input type="text" placeholder="e.g. Kyläsaarenkuja 5 B" name="address" required></input>
            <label for="zip"><b>ZIP Code</b></label>
            <input type="text" placeholder="e.g. 00220" name="zip" required></input>
        </div>
    )
}

function RegisterRequester() {
    return (
        <form>
            <input type="hidden" name="usertype" value="requester" />
            <RegisterShared />
            <AddressPart />
            <button type="register">Register</button>
            <br />
        </form>
    )
}

function RegisterVolunteer() {
    return (
        <form>
            <input type="hidden" name="usertype" value="volunteer" />
            <RegisterShared />
            <button type="register">Register</button>
        </form>
    )
}

function RegisterShowOwner() {
    return (
        <form>
            <input type="hidden" name="usertype" value="shopowner" />
            <RegisterShared />
            <button type="register">Work in progress</button>
        </form>
    )
}

function LoginUserTypeSelector() {
    let types = ['Volunteer', 'Requester', 'ShowOwner']
    let labels = ['Volunteer', 'Requester', 'Show owner']
    return (
        <div>
            I am a...
            <select>
                {types.map((type, idx) => <option key={type}>{labels[idx]}</option>)}
            </select>
        </div>
    )
}

export default Login;