import React, {useState} from "react";
import {redirect, useNavigate} from "react-router-dom";
import Backend from '../api';

export default function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate()

    const onFormSubmit = (event) => {
        event.preventDefault();
    
        onLogin(username, password)
        
      };

    const onLogin = async (username, password) => {
        const response = await Backend.post(
            '/login', {
                    username: username,
                    password: password
    }).then( (res) => {
        console.log(res)
        // if (res['data']['created']){
        //     alert("Authenticated Successfully.")
        //     navigate("/");
        // } else {
        //     alert("Could not log in")
        // }
    
    })}

    return (
    <form onSubmit={onFormSubmit}>
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