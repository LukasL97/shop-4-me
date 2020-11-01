import React from 'react'
import PropTypes from 'prop-types'

import { errorStyles } from './errorStyles'
const TextInputField = ({
  label,
  id,
  type,
  name,
  value,
  placeholder,
  onChange,
  onBlur,
  error,
  checked,
  className,
}) => {
  const invalidInput = error ? 'invalid-input' : ''
  if (type === 'radio') {
    return (
      <div className={'field'}>
        <div className='control'>
          <input
            type={type}
            name={name}
            id={id}
            value={value}
            onChange={onChange}
            onBlur={onBlur}
            checked={checked}
            className='input'
          />
        </div>
        {label && (
          <label htmlFor={id} className='input-label label'>
            {label}
          </label>
        )}
        {error && (
          <small style={errorStyles} className='error invalid-feedback'>
            {error}
          </small>
        )}
      </div>
    )
  } else if (type === 'checkbox') {
    const styles = {
      display: 'flex',
      border: '5px solid green',
      color: 'red',
      alignItems: 'center',
      border: '5px solid red',
    }
    return (
      <div className={'form-checkbox-group'}>
        <label htmlFor=''>
          <input
            type={type}
            name={name}
            id={name}
            value={value}
            onChange={onChange}
            onBlur={onBlur}
            checked={checked}
          />
          {label && <label htmlFor={name}>{label}</label>}
        </label>
      </div>
    )
  }

  return (
    <div className={className ? className : 'form-group field'}>
      {label && (
        <label htmlFor={name} className='label'>
          {label}
        </label>
      )}
      <div className='control'>
        <input
          type={type}
          name={name}
          id={name}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          onBlur={onBlur}
          className={invalidInput + ' input'}
        />
      </div>

      {error && (
        <small className='error' style={errorStyles}>
          {error}
        </small>
      )}
    </div>
  )
}
TextInputField.defaultProps = {
  type: 'text',
  placeholder: '',
}
TextInputField.propTypes = {
  type: PropTypes.string,
  name: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
}

export default TextInputField
