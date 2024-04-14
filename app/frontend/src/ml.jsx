import './ml.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ML() {
  const [response, setResponse] = useState({});

  useEffect(() => {
    axios.get('https://sarezgitiba.lv/api/sarezgitiba/2')
      .then(response => {
        setResponse(response.data);
        console.log(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  return (
    <div>
      <p>hello there! :3 faq</p>
    </div>
    );
  }

export default ML;
