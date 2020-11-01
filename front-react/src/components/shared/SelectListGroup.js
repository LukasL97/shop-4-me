import React from 'react'
import PropTypes from 'prop-types'
import classnames from 'classnames'

import { errorStyles } from './errorStyles'

const SelectListGroup = ({
  label,
  htmlFor,
  name,
  value,
  error,
  info,
  onChange,
  options,
}) => {
  const selectOptions = options.map((option) => (
    <option key={option.label} value={option.value}>
      {option.label}
    </option>
  ))
  return (
    <div className=' field'>
      <label htmlFor={htmlFor}>{label}</label>
      <span className='select'>
        <select
          className={classnames('form-control form-control-lg', {
            'is-invalid': error,
          })}
          name={name}
          value={value}
          onChange={onChange}
        >
          {selectOptions}
        </select>
      </span>
      {info && <small className='form-text text-muted'>{info}</small>}
      {error && (
        <small className='invalid-feedback' style={errorStyles}>
          {error}
        </small>
      )}
    </div>
  )
}

SelectListGroup.propTypes = {
  name: PropTypes.string.isRequired,
  value: PropTypes.string.isRequired,
  info: PropTypes.string,
  error: PropTypes.string,
  onChange: PropTypes.func.isRequired,
  options: PropTypes.array.isRequired,
}

export default SelectListGroup
