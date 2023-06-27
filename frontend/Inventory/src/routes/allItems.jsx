import React, {useState} from "react";
import {redirect, useNavigate} from "react-router-dom";
import Backend from '../api';
import ItemCard from "../itemCard"


export default function ShowAllItems() {
    const [items, setItems] = useState([]);

    const getItems = async () => {
        const response = await Backend.get(
            '/items', {}).then( (res) => {setItems(res['data'])})}

    if (items.length == 0){
        getItems()
    }
    
    return (
        <div class="container">
<div class="row flex-row">
        {items.map(item => ItemCard(item))}
</div>
        </div>
    );
  }