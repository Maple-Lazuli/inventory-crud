import React, {useState} from "react";
import {redirect, useNavigate} from "react-router-dom";
import Backend from '../api';
import {getUsername, getAccountID, getSession} from '../credentials'
import ItemCardOwned from "../itemCardOwned"



export default function OwnedItems() {
    const [items, setItems] = useState([]);
    const [accountID, setAccountID] = useState(-1);

    const [session, setSession] = useState("");
    const [username, setUserName] = useState("");

    getSession().then(s => setSession(s))
    getUsername().then(u => setUserName(u))


    const getItems = async () => {
        const response = await Backend.get(
            '/items', {}).then( (res) => {
                setItems(res['data'].filter(item => item.account_id == accountID))
            })}

    const getAccount = async() => {
        getAccountID().then(i => setAccountID(i))
    }


    if (items.length == 0){
        getAccount()
        getItems()
    }
    
    return (
        <div class="container">
            <a class="btn btn-primary" href="/CreateItem" role="button">Add Item</a>
            <hr />
        <div class="row flex-row">
        {items.map(item => ItemCardOwned(item, session, username))}
        </div>
        </div>
    );
  }