import React, { Component } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
class UserStatus extends Component {
  constructor(props) {
    super(props);
    this.state = {
      email: '',
      id: '',
      username: '',
      active: '',
      admin: '',
    }
  }
  componentDidMount() {
    if (this.props.isAuthenticated){
      this.getUserStatus();
    }
  }
  getUserStatus() {
    const options = {
      url: `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/status`,
      method: 'get',
      headers: {
        'Content-Type':'application/json',
        Authorization:`Bearer ${window.localStorage.authToken}`
      }
    };
    return axios(options)
                .then((res)=>{
                  this.setState({...res.data.data});
                })
                .catch((err)=>{
                  console.log(err);
                })
  }
  render() {
    if (!this.props.isAuthenticated){
      return (<div>
        <p>You must be logged in to view this! Click <Link to="/login">here</Link> to
log back in.</p>
        </div>)
    }
    return (
      <div>
        <ul>
          <li><strong>User ID:</strong> {this.state.id}</li>
          <li><strong>Email:</strong> {this.state.email}</li>
          <li><strong>Username:</strong> {this.state.username}</li>
          <li><strong>Admin:</strong> {String(this.state.admin)}</li>
          <li><strong>Active:</strong> {String(this.state.active)}</li>
        </ul>
      </div>
    );
  }

}

export default UserStatus;
