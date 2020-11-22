import React, { useState } from 'react'
import axios from 'axios'
import TextInputField from './shared/TextInputField'
import Layout from './Layout'
import '../assets/styles/add-item.scss'
import '../assets/styles/buttons.scss'
import '../assets/styles/input-file.scss'
import Cookies from 'universal-cookie'

const AddShop = (props) => {
	const [formData, setFormData] = useState({
		name: "",
		street: "",
		zip: "",
		country: "Finland"
	})

	const onChange = (e) => {
		let data = { ...formData }
		data[e.target.name] = e.target.value
		setFormData(data)
	}
	const onSubmit = async (e) => {
	  e.preventDefault()
      const cookies = new Cookies()
      //if (cookies.get('user_type') != 'ShopOwner') { return }
		
	  let response = await axios.post('http://localhost:5000/shop', {
        name: formData.name,
        address: {
          street: formData.street,
          zip: formData.zip,
          country: formData.country
		},
        sessionId: cookies.get('access_token')
	  })
	  console.log(response)
	
      props.history.push('/')
	}
	return (
		<Layout>
		  <div className='add-item-container'>
			<form onSubmit={onSubmit} noValidate>
				<TextInputField
				  label='Name'
				  id='name'
				  type='text'
				  name='name'
				  value={formData.name}
				  onChange={onChange}
				  placeholder='e.g. K-Neste Pacifiuksenkatu 25'
				/>
				<TextInputField
				  label='Street'
				  id='street'
				  type='text'
				  name='street'
				  value={formData.street}
				  onChange={onChange}
				  placeholder='e.g. Pacifiuksenkatu 25'
				/>
				<TextInputField
				  label='Zip'
				  id='zip'
				  type='text'
				  name='zip'
				  value={formData.zip}
				  onChange={onChange}
				  placeholder='e.g. 00530'
				/>
			  <TextInputField
				label='Country'
				id='country'
				type='text'
				name='country'
				value={formData.country}
				onChange={onChange}
				placeholder='e.g. Finland'
			  />
			  <button className='btn' type='submit' id='submit-button'>
				Add Shop
			  </button>
			</form>
		  </div>
		</Layout>)
}

export default AddShop