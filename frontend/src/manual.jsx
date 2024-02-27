import './manual.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Manual() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    axios.get('https://sarezgitiba.lv/api/sarezgitiba/3')
      .then(response => {
        setPosts(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);
  return (
    <div>
      <p>hello there! :3 manual</p>
    </div>
    );
  }

export default Manual;