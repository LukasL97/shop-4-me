import axios from 'axios';
import React from 'react';
import Cookies from 'universal-cookie';

var ReactRouter = require('react-router-dom');

function Login() {
	let history = ReactRouter.useHistory()
	
	function gotoHome() {
		history.push('/')
	}

    return (
        <div className='login'>
            <section className="section">
                <h1 className="title">Welcome to <strong>Shop-4-Me</strong></h1>
                <h2 className="title">Friendly neighborhood shopping assistant</h2>
                <LoginUserTypeSelector />
                <LoginSignIn to={gotoHome}/>
            </section>
            <section className="section">
                <LoginRegister to={gotoHome}/>
            </section>
        </div>
    )
}

function LoginSignIn({to}) {

    function handleSubmit(event) {
        event.preventDefault();
        let data = {
            userType: "Requester",
            loginName: event.target.email.value,
            password: event.target.password.value
        }
        console.log(data);

        var callback = (res) => {
            console.log(res)
            const cookies = new Cookies();
            cookies.set('access_token', res.data, { path: '/', expires: new Date(new Date().getTime() + 60 * 60 * 1000) })
            to()
        }

        axios.post("http://localhost:5000/login", data).then(callback)
    }

    return (
        <form onSubmit={handleSubmit}>
            <InputField
                name="email" label="Email" type="email" placeholder="e.g. email@provider.com" required />
            <InputField
                name="password" label="Password" type="password" placeholder="e.g. iSecretlyLove50Cent" required />
            <button className="button is-link" type="submit">Login</button>
        </form>
    )
}

function LoginRegister({to}) {

    function handleSubmit(event) {
		event.preventDefault();
        let data = {
            userType: event.target.usertype.value,
            loginName: event.target.email.value,
            password: event.target.password.value,
            firstName: event.target.firstname.value,
            lastName: event.target.lastname.value
        }

        var callback = (res) => {
			console.log(res);
            const cookies = new Cookies();
            cookies.set('access_token', res.data, { path: '/', expires: new Date(new Date().getTime() + 60 * 60 * 1000) })
			to()
		}
        axios.post("http://localhost:5000/register", data).then(callback)
    }

    let component = RegisterRequester()

    return (
        <form onSubmit={handleSubmit}>
            {component}
        </form>
    )

}

function InputField({name, label, type, placeholder, iconr, iconl, error_message, ok_message, required}) {
    var input_class =  error_message ? "is-danger" : ok_message ? "is-success" : ""
    var below_text = error_message ? <p className="help is-danger">{error_message}</p> :
                     ok_message ? <p className="help is-success">{ok_message}</p> :
                     null
    var icon_container_class = ""
    var right_icon = null
    var left_icon = null
    if (iconr) {
        icon_container_class += " has-icons-right"
        right_icon = (
            <span className="icon is-small is-right">
                <i className={"fas " + iconr}></i>
            </span>
        )
    }
    if (iconl) {
        icon_container_class += " has-icons-left"
        left_icon = (
            <span className="icon is-small is-left">
                <i className={"fas " + iconl}></i>
            </span>
        )
    }
    required = required ? true : false //cast to boolean
    return (
        <div className="field">
            <label htmlFor={name} className="label">{label}</label>
            <div className={"control" + icon_container_class}>
                <input name={name} className={"input " + input_class} type={type} placeholder={placeholder} required={required} />
                {left_icon}
                {right_icon}
            </div>
            {below_text}
        </div>
    )
}

function RegisterSharedUpper() {
    return (
        <div>
            <InputField
                name="firstname" label="First name" type="text" placeholder="Firsty" required />
            <InputField
                name="lastname" label="Last name" type="text" placeholder="Lastnamersson" required />
            <InputField
                name="email" label="Email" type="email" placeholder="e.g. email@provider.com"
                iconl="fa-envelope" iconr="fa-check" ok_message="This username is available" required />
            <InputField
                name="password" label="Password" type="password" placeholder="e.g. something614SortaSecure"
                iconl="fa-user" error_message="Password is too short!" required />
        </div>
    )
}

function RegisterSharedLower() {
    return (
        <div>
            <div className="field">
                <div className="control">
                    <label className="checkbox">
                        <input type="checkbox" /> I agree to the <a href="#">terms and conditions</a>
                    </label>
                </div>
            </div>
            <div className="field">
                <div className="control">
                    <button className="button is-link" type="submit">Register</button>
                </div>
            </div>
        </div>
    )
}

function RegisterAddressPart() {
    return (
        <>
            <InputField
                name="address" label="Street address" type="text" placeholder="e.g. Kyläsaarenkuja 5 B" required />
            <InputField
                name="zip" label="ZIP Code" type="number" placeholder="e.g. 00220" required />
        </>
    )
}

function RegisterRequester() {
    return (
        <>
            <input type="hidden" name="usertype" value="Requester" />
            <RegisterSharedUpper />
            <RegisterAddressPart />
            <RegisterSharedLower />
        </>
    )
}

function RegisterVolunteer() {
    return (
        <>
            <input type="hidden" name="usertype" value="Volunteer" />
            <RegisterSharedUpper />
            <RegisterSharedLower />
        </>
    )
}

function RegisterShowOwner() {
    return (
        <>
            <input type="hidden" name="usertype" value="ShopOwner" />
            <RegisterSharedUpper />
            <RegisterSharedLower />
        </>
    )
}

function LoginUserTypeSelector() {
    let types = ['Volunteer', 'Requester', 'ShowOwner']
    let labels = ['Volunteer', 'Requester', 'Show owner']
    return (
        <div className="field">
          <label className="label">I am a...</label>
          <div className="control">
            <div className="select">
              <select>
                {types.map((type, idx) => <option key={type}>{labels[idx]}</option>)}
              </select>
            </div>
          </div>
        </div>
    )
}

export default Login;