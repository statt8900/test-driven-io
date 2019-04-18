import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import UsersList from './components/UsersList';
import AddUser from './components/AddUser';


class App extends Component {
  constructor(props){
    super(props)
    this.state = {
      users : [],
      username : 'test',
      email: 'test@test.com',
      err: {showAlert:false,message:''},
    }
    this.getUsers     = this.getUsers.bind(this)
    this.addUser      = this.addUser.bind(this)
    this.handleChange = this.handleChange.bind(this)
  }
  componentDidMount() {
    this.getUsers()
  }
  getUsers(){
    axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
         .then((res)=>{this.setState({users:res.data.data.users})})
         .catch((err)=>{console.log(err)})
  }
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
  render() {
    return (
      <section className="section">
        <div className="container">
          <div className="row">
            <div className="col-md-4">
              <br/>
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
          </div>
        </div>
      </section>
    );
  }

}

ReactDOM.render(<App />, document.getElementById('root'));
