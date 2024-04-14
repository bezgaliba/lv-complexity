import './manual.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';
import React, { useState } from 'react';
import { Link } from "react-router-dom";
import axios from 'axios';

function Manual() {
  const [data, setData] = useState([]);
  const [text, setText] = useState('');
  const [key, setKey] = useState('home');
  const [loading, setLoading] = useState(false); 
  // const [loadingScreen, setLoadingScreen] = useState(false);
  

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.get(`https://sarezgitiba-flask-yhf42gzwra-lm.a.run.app/untrained_predict?text=${text}`);
      const data = response.data;
      setData(data);
      setLoading(true);
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      {/* { loadingScreen && (
      <div className="spinner-container">
        <div className="spinner"></div>
      </div>
      )}; */}
      <div className="split left">
        <div className="centered">
          <h2 className="headerIn">Ievads</h2>
          <p className="instructionsTop">Ievadiet tekstu, kuras sarežģītību novērtēt ar modeli:</p>
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
      <h1 className="headerOverlap">ML teikuma sarežģītība</h1>
  
      <div className="split right">
        <div className="centered">
            <h2 className="header">Izvade</h2>
            <div className="rougeScoresContainer">
            {loading && (
              <div>
                <p>Dots teksts: <b>{data.text}</b></p>
                <p>Šis teksts tiek atpazīts kā <b>{data.prediction}</b>. klases teksts</p>
              </div>
            )}
            </div>
          </div>
        </div>
      </div>
  );
  }
  



export default Manual;