import React from 'react';

const inputClass = "input is-large";

const AddUser = (props) =>{
  return (
    <form
      onSubmit={(event)=>props.addUser(event)}
    >
      <div className="field">
        <input
          name="username"
          className={inputClass}
          type="text"
          value = {props.username}
          onChange={(event)=>props.handleChange(event)}
          placeholder="Enter a username"
          required
        />
      </div>
      <div className="field">
        <input
          name="email"
          className={inputClass}
          type="email"
          placeholder="Enter a email"
          value = {props.email}
          onChange={(event)=>props.handleChange(event)}
          required
        />
      </div>
      <div className="field">
        <input
          name="submit"
          type="submit"
          className="button is-primary is-large is-fullwidth"
          value="Submit"
        />
      </div>
    </form>
  )
}

export default AddUser
