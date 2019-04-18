import React from 'react';

const UsersList = (props) => (
  <div>
    {
      props.users.map((user) => {
        return (
          <h4
            key={user.id}
            className="well"
          >{user.email}
          </h4>
        )
      })
    }
  </div>
);

export default UsersList;
