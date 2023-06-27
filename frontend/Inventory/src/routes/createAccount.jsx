import React, {useState} from "react";
import {redirect, useNavigate} from "react-router-dom";
import Backend from '../api';

export default function CreateAccount() {
    const [firstname, setFirstname] = useState("");
    const [lastname, setLastname] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate()

    const onFormSubmit = (event) => {
        event.preventDefault();
    
        onAccountSubmit(firstname, lastname, username, password, 1)
        
      };

    const onAccountSubmit = async (firstname, lastname, username, password, role) => {
        const response = await Backend.post(
            '/account', {
                    role_id:role,
                    first_name: firstname,
                    last_name: lastname,
                    username: username,
                    password: password
    }).then( (res) => {
        
        if (res['data']['created']){
            alert("Account Created Successfully.")
            navigate("/");
        } else {
            alert("Account Could Not Be Created.")
        }
    
    })}

    return (
    <form onSubmit={onFormSubmit}>
        <div className="mb-3">
        <label htmlFor="firstname" className="form-label">First Name</label>
        <input type="text" className="form-control" id="firstname" placeholder=""
        onChange={() => setFirstname(event.target.value)}/>
        </div>
        <div className="mb-3">
        <label htmlFor="lastname" className="form-label">Last Name</label>
        <input type="text" className="form-control" id="lastname" placeholder=""
        onChange={() => setLastname(event.target.value)}/>
        </div>
        <div className="mb-3">
        <label htmlFor="username" className="form-label">User Name</label>
        <input type="text" className="form-control" id="username" placeholder=""
        onChange={() => setUsername(event.target.value)}/>
        </div>
            <div className="mb-3">
                <label htmlFor="exampleInputPassword1" className="form-label">Password</label>
                <input type="password" className="form-control" id="exampleInputPassword1"
                onChange={() => setPassword(event.target.value)}/>
            </div>
            <button type="submit" className="btn btn-primary">Create Account</button>
    </form>
    );
  }