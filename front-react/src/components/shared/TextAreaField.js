import React from 'react'
import PropTypes from 'prop-types'
import classnames from 'classnames'

import { errorStyles } from './errorStyles'
const TextAreaFieldGroup = ({
  label,
  name,
  placeholder,
  value,
  disabled,
  onChange,
  error,
  className,
  info,
  cols,
  rows,
}) => {
  const invalidInput = error ? 'invalid-input' : ''
  return (
    <div className='form-group'>
      {label && <label>{label}</label>}
      <textarea
        name={name}
        value={value}
        placeholder={placeholder}
        className={classnames(
          `form-control form-control-lg ${className} ${invalidInput}`,
          {
            'is-invalid': error,
          }
        )}
        disabled={disabled}
        onChange={onChange}
        cols={cols}
        rows={rows}
      />
      {info && (
        <small
          style={{ fontWeight: 'lighter' }}
          className='form-text text-muted'
        >
          {' '}
          {info}{' '}
        </small>
      )}
      {error && (
        <small style={errorStyles}  className='error invalid-feedback'>
          {' '}
          {error}{' '}
        </small>
      )}
    </div>
  )
}

TextAreaFieldGroup.propTypes = {}

export default TextAreaFieldGroup
