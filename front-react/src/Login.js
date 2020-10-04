import React from 'react';
import Cookies from 'universal-cookie';

var ReactRouter = require('react-router-dom');

function Login() {
    let history = ReactRouter.useHistory()

    return (
        <div className='login'>
            <section class="section">
                <h1 class="title">Welcome to <strong>Shop-4-Me</strong></h1>
                <h2 class="title">Friendly neighborhood shopping assistant</h2>
                <LoginUserTypeSelector />
                <LoginSignIn />
            </section>
            <section class="section">
                <LoginRegister />
            </section>
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
            <InputField
                name="email" label="Email" type="email" placeholder="e.g. email@provider.com" required />
            <InputField
                name="password" label="Password" type="password" placeholder="e.g. iSecretlyLove50Cent" required />
            <button class="button is-link" type="submit">Login</button>
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

function InputField({name, label, type, placeholder, iconr, iconl, error_message, ok_message, required}) {
    var input_class =  error_message ? "is-danger" : ok_message ? "is-success" : ""
    var below_text = error_message ? <p class="help is-danger">{error_message}</p> :
                     ok_message ? <p class="help is-success">{ok_message}</p> :
                     null
    var icon_container_class = ""
    var right_icon = null
    var left_icon = null
    if (iconr) {
        icon_container_class += " has-icons-right"
        right_icon = (
            <span class="icon is-small is-right">
                <i class={"fas " + iconr}></i>
            </span>
        )
    }
    if (iconl) {
        icon_container_class += " has-icons-left"
        left_icon = (
            <span class="icon is-small is-left">
                <i class={"fas " + iconl}></i>
            </span>
        )
    }
    required = required ? true : false //cast to boolean
    return (
        <div class="field">
            <label for={name} class="label">{label}</label>
            <div class={"control" + icon_container_class}>
                <input name={name} class={"input " + input_class} type={type} placeholder={placeholder} required={required} />
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
            <div class="field">
                <div class="control">
                    <label class="checkbox">
                        <input type="checkbox" /> I agree to the <a href="#">terms and conditions</a>
                    </label>
                </div>
            </div>
            <div class="field">
                <div class="control">
                    <button class="button is-link" type="submit">Register</button>
                </div>
            </div>
        </div>
    )
}

function AddressPart() {
    return (
        <div>
            <InputField
                name="address" label="Street address" type="text" placeholder="e.g. Kyläsaarenkuja 5 B" required />
            <InputField
                name="zip" label="ZIP Code" type="number" placeholder="e.g. 00220" required />
        </div>
    )
}

function RegisterRequester() {
    return (
        <form>
            <input type="hidden" name="usertype" value="requester" />
            <RegisterSharedUpper />
            <AddressPart />
            <RegisterSharedLower />
        </form>
    )
}

function RegisterVolunteer() {
    return (
        <form>
            <input type="hidden" name="usertype" value="volunteer" />
            <RegisterSharedUpper />
            <RegisterSharedLower />
        </form>
    )
}

function RegisterShowOwner() {
    return (
        <form>
            <input type="hidden" name="usertype" value="shopowner" />
            <RegisterSharedUpper />
            <RegisterSharedLower />
        </form>
    )
}

function LoginUserTypeSelector() {
    let types = ['Volunteer', 'Requester', 'ShowOwner']
    let labels = ['Volunteer', 'Requester', 'Show owner']
    return (
        <div class="field">
          <label class="label">I am a...</label>
          <div class="control">
            <div class="select">
              <select>
                {types.map((type, idx) => <option key={type}>{labels[idx]}</option>)}
              </select>
            </div>
          </div>
        </div>
    )
}

export default Login;