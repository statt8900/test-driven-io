import React from 'react';
// import Alert from 'react-bootstrap';
const inputClass = "form-control";

const AddUser = (props) =>{
  return (
    <div className="well">
      <legend>Add User</legend>
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
        <br />
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
        <br />
        <div className="field">
          <input
            name="submit"
            type="submit"
            className="btn btn-primary mb-2"
            value="Submit"
          />
        </div>
      </form>
      {props.showAlert ? <div><br/><div className="alert alert-danger" role="alert">{props.errMessage}</div></div> : null}
    </div>
  )
}

export default AddUser
