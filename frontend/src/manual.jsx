import './manual.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState, useEffect } from 'react';
import { Link } from "react-router-dom";
import axios from 'axios';

function Manual() {
  const [data, setData] = useState([]);
  const [text, setText] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.get(`https://sarezgitiba-flask-yhf42gzwra-lm.a.run.app/?text=${text}`);
      const data = response.data;
      setData(data)
      console.log(data)
    } catch (error) {
      console.error(error);
    }
  };

  
  return (
    <div>
      {/* { loading && */}
      <div className="spinner-container">
        <div className="spinner"></div>
      </div>
      {/* } */}
      <h1 className="headerOverlap">Manuālā teikuma sarežģītība</h1>
      <div className="split left">
        <div className="centered">
          <h2 className="headerIn">Ievads</h2>
          <p className="instructionsTop">Ievadiet tekstu, kuras sarežģītību novērtēt:</p>
          <form onSubmit={handleSubmit}>
            <textarea
              className="textbox"
              value={text}
              onChange={(e) => setText(e.target.value)}
            />
            <button className="button" type="submit">Aiziet!</button>
          </form>
        </div>
        <Link to="/" className='button back'>Atpakaļ!</Link>
      </div>
    
      <div className="split right">
        <div className="centered">
            <h2 className="header">Izvade</h2>
            <div className="rougeScoresContainer">
              <p>LV meginajuma koeficients: {data.lv_meginajuma_koef}</p>
              <p>LV meginajuma klase: {data.lv_meginajuma_klase}</p>
            </div>
            {data.zilbju_saraksts?.map((item, index) => (
              <p key={index}>{item}</p>
            ))
            }
        </div>
      </div>
    </div>
    );
  }



export default Manual;