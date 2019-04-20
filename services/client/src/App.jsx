import React, { Component } from 'react';
import { Route, Switch } from 'react-router-dom';
import axios from 'axios';

import NavBar from './components/NavBar';
import UsersList from './components/UsersList';
import AddUser from './components/AddUser';
import Form from './components/Form';
import About from './components/About';
import Logout from './components/Logout';
import UserStatus from './components/UserStatus';

class App extends Component {
  constructor(props){
    super(props)
    this.state = {
      title: 'Hello World!',
      users : [],
      username : 'test',
      email: 'test@test.com',
      isAuthenticated: false,
      formData:{
        'username': 'test',
        'email':'new@new.com',
        'password':'test'
      },
      err: {showAlert:false,message:''},
    }

    // bind this to all the methods
    this.getUsers     = this.getUsers.bind(this)
    this.addUser      = this.addUser.bind(this)
    this.handleChange = this.handleChange.bind(this)
    this.handleFormChange = this.handleFormChange.bind(this)
    this.handleUserFormSubmit = this.handleUserFormSubmit.bind(this)
    this.logoutUser = this.logoutUser.bind(this)
  }
  componentDidMount() {
    // Once component mounts perform ajax
    this.getUsers()
  }
  getUsers(){
    // Get all users
    axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
         .then((res)=>{this.setState({users:res.data.data.users})})
         .catch((err)=>{console.log(err)})
  }
  // Add Users methods
  handleChange(event){
      const obj = {};
      obj[event.target.name] = event.target.value;
      this.setState(obj);
  }
  addUser(event){
    event.preventDefault();
    console.log('Sanity Check!')
    console.log(this.state)
    axios.post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`,
              {username:this.state.username, email:this.state.email}
              )
         .then((res)=>{
           this.getUsers()
           this.setState({ username: '', email: '', err:{showAlert:false,message:''} });
         })
         .catch((err)=>{console.log(err.response.data.message);this.setState({err:{showAlert:true,message:err.response.data.message}})})
  }
  // Form component methods
  handleFormChange(event){
    const obj = this.state.formData;
    obj[event.target.name] = event.target.value;
    this.setState({'formData':obj})
  }
  handleUserFormSubmit(event){
    event.preventDefault();
    const formType = window.location.href.split('/').reverse()[0];
    let data = {
      'email':this.state.formData.email,
      'password':this.state.formData.password
    }
    if (formType === 'register'){
      data['username'] = this.state.formData.username
    }
    console.log(data)
    const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/${formType}`;
    axios.post(url,data)
         .then((res)=>{
           this.setState({
             formData: {username:'',email:'',password:''},
             email: '',
             username:'',
             isAuthenticated: true
           })
           this.getUsers();
           console.log(this.state)
           window.localStorage.setItem('authToken', res.data.auth_token);
         })
         .catch((err)=>{
           console.log(err)
         })
  }
  // Log out methods
  logoutUser(){
    window.localStorage.clear()
    this.setState({
      isAuthenticated: false
    })
    // axios.post(url,data)
    //      .then((res)=>{

    //        console.log('Logged out')
    //      })
    //      .catch((err)=>{
    //        console.log(err)
    //      })
  }
  render() {
    return (
      <section className="section">
        <NavBar title={this.state.title} isAuthenticated={this.state.isAuthenticated}/>
        <div className="container">
          <div className="row">
            <div className="col-md-4">
              <br/>
              <Switch>
                <Route exact path='/' render={()=>(
                  <div>
                    <h1 className="">All Users</h1>
                    <hr/><br/>
                    <UsersList users={this.state.users} />
                    <br/><br/>
                    <AddUser
                      addUser={this.addUser}
                      handleChange={this.handleChange}
                      username={this.state.username}
                      email={this.state.email}
                      showAlert={this.state.err.showAlert}
                      errMessage={this.state.err.message}
                    />
                  </div>
                )}/>
                <Route exact path='/about' render={()=>(
                  <About />
                )}/>
                <Route exact path='/register' render={()=>(
                  <Form
                    formType={'Register'}
                    formData={this.state.formData}
                    handleFormChange={this.handleFormChange}
                    handleUserFormSubmit={this.handleUserFormSubmit}
                    isAuthenticated={this.state.isAuthenticated}
                  />
                )}/>
                <Route exact path='/status' render={()=>(
                  <UserStatus isAuthenticated={this.state.isAuthenticated}/>
                )}/>
                <Route exact path='/login' render={()=>(
                  <Form
                    formType={'Login'}
                    formData={this.state.formData}
                    handleFormChange={this.handleFormChange}
                    handleUserFormSubmit={this.handleUserFormSubmit}
                    isAuthenticated={this.state.isAuthenticated}
                  />
                )}/>
                <Route exact path='/logout' render={()=>(
                  <Logout
                    logoutUser={this.logoutUser}
                    isAuthenticated={this.state.isAuthenticated}
                  />
                )}/>
              </Switch>
            </div>
          </div>
        </div>
      </section>
    );
  }

}

export default App;
