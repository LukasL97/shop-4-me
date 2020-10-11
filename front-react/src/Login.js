import axios from 'axios'
import React, { useState } from 'react'
import Cookies from 'universal-cookie'
import Layout from './components/Layout'

var ReactRouter = require('react-router-dom')

function Login() {
	let history = ReactRouter.useHistory()
	const [registerComponent, setRegisterComponent] = useState(<RegisterVolunteer />);
	
	function gotoHome() {
		history.push('/')
	}

    return (
		<Layout>
			<div className='login'>
				<section className="section">
					<h1 className="title">Welcome to <strong>Shop-4-Me</strong></h1>
					<h2 className="title">Friendly neighborhood shopping assistant</h2>
					<LoginUserTypeSelector setRegisterComponent={setRegisterComponent}/>
					<LoginSignIn to={gotoHome}/>
				</section>
				<section className="section">
					<LoginRegister to={gotoHome} registerComponent={registerComponent}/>
				</section>
			</div>
    	</Layout>
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
				name='email'
				label='Email'
				type='email'
				placeholder='e.g. email@provider.com'
				required
			/>
			<InputField
				name='password'
				label='Password'
				type='password'
				placeholder='e.g. iSecretlyLove50Cent'
				required
			/>
			<button className='button is-link' type='submit'>
				Login
			</button>
		</form>
	)
}

function LoginRegister({to, registerComponent}) {

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
	
    return (
        <form onSubmit={handleSubmit}>
            {registerComponent}
        </form>
    )
}

class InputField extends React.Component {

  constructor(props){ //{ name, label, type, placeholder, iconr, iconl, error_message, ok_message, inputCheck, required }
	super(props);
   
	this.state = {
		error_message: props.error_message,
		ok_message: props.ok_message,
		iconr: props.iconr,
		iconl: props.iconl
	}
  }

  handleOnChange(event) {
	if (this.props.inputCheck) {
		let result = this.props.inputCheck(event.target.value)
		this.setState({
			...this.state,
			...result
		})
		console.log(this.state)
	}
  }

  render() {
	var input_class = ''
	var below_text = null
  
	input_class = this.state.error_message ? 'is-danger' : this.state.ok_message ? 'is-success' : ''
	below_text = this.state.error_message ? (
		<p className='help is-danger'>{this.state.error_message}</p>
	) : this.state.ok_message ? (
		<p className='help is-success'>{this.state.ok_message}</p>
	) : null
  
	var icon_container_class = ''
	var right_icon = null
	var left_icon = null
	var required = this.props.required ? true : false //cast to boolean
  
	icon_container_class = ''
	right_icon = null
	left_icon = null
	if (this.state.iconr) {
		icon_container_class += ' has-icons-right'
		right_icon = (
		<span className='icon is-small is-right'>
			<i className={'fas ' + this.state.iconr}></i>
		</span>
		)
	}
	if (this.state.iconl) {
		icon_container_class += ' has-icons-left'
		left_icon = (
		<span className='icon is-small is-left'>
			<i className={'fas ' + this.state.iconl}></i>
		</span>
		)
	}

	return (
		<div className='field'>
		<label htmlFor={this.props.name} className='label'>
			{this.props.label}
		</label>
		<div className={'control' + icon_container_class}>
			<input
			name={this.props.name}
			className={'input ' + input_class}
			type={this.props.type}
			placeholder={this.props.placeholder}
			onChange={(event) => this.handleOnChange(event)}
			required={required}
			/>
			{left_icon}
			{right_icon}
		</div>
		{below_text}
		</div>
	)
  }
}

function RegisterSharedUpper() {
  return (
    <div>
      <InputField
        name='firstname'
        label='First name'
        type='text'
        placeholder='Firsty'
        required
      />
      <InputField
        name='lastname'
        label='Last name'
        type='text'
        placeholder='Lastnamersson'
        required
      />
      <InputField
        name='email'
        label='Email'
        type='email'
        placeholder='e.g. email@provider.com'
        iconl='fa-envelope'
		inputCheck={(email) => {
			return email ? {
				ok_message: 'This username is available',
				iconr: 'fa-check'
			} : {
				ok_message: null,
				iconr: null
			}
		}}
        required
      />
      <InputField
        name='password'
        label='Password'
        type='password'
        placeholder='e.g. something614SortaSecure'
		iconl='fa-user'
		inputCheck={(password) => {
			return password.length < 7 ? {
				ok_message: null,
				error_message: 'Password is too short!',
				iconr: null
			} : {
				ok_message: ' ',
				error_message: null,
				iconr: 'fa-check'
			}
		}}
        required
      />
    </div>
  )
}

function RegisterSharedLower() {
    return (
        <>
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
        </>
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

function LoginUserTypeSelector({ setRegisterComponent }) {
	let selections = [
		{ label: 'Volunteer',  registerComponent: <RegisterVolunteer /> },
		{ label: 'Requester',  registerComponent: <RegisterRequester /> },
		{ label: 'Shop owner', registerComponent: <RegisterShowOwner /> }
	]

	function handleOnChange(event) {
		setRegisterComponent(selections[event.target.value].registerComponent)
	}

  return (
    <div className='field'>
      <label className='label'>I am a...</label>
      <div className='control'>
        <div className='select'>
          <select onChange={handleOnChange}>
            {selections.map((data, idx) => (
              <option key={idx} value={idx}>{data.label}</option>
            ))}
          </select>
        </div>
      </div>
    </div>
  )
}

export default Login
