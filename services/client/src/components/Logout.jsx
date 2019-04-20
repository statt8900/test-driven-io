import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class Logout extends Component {
  componentDidMount() {
    this.props.logoutUser();
  }
  render() {
    const message = <p>You are now logged out. Click <Link to="/login">here</Link> to log back in</p>;;
    return (
      <div>
        { message }
      </div>
    );
  }

}

export default Logout;
