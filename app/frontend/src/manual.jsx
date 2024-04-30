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
      const response = await axios.get(`https://sarezgitiba-flask-yhf42gzwra-lm.a.run.app/statistics?text=${text}`);
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
      <h1 className="headerOverlap">Teksta statistikas sarežģītība</h1>
  
      <div className="split right">
        <div className="centered">
            <h2 className="header">Izvade</h2>
            <div className="rougeScoresContainer">
            {loading && (
              <div>
                <p>Dots teksts: <b>{data.teksts}</b></p>
                <Tabs
                  activeKey={key}
                  onSelect={(k) => setKey(k)}
                  className="mb-3"
                  fill
                  variant="underline"
                >
                  <Tab eventKey="home" title="Kvantitatīvie rādītāji">
                  {/* <p>Fleša-Kincaida lasīšanas viegluma klase: <b>{data.flesch_klase}</b></p>
                  <p>Fleša-Kincaida lasīšanas viegluma aprēķins: <b>{data.flesch_koef}</b></p>
                  <p>Gunninga "miglas" indekss: <b>{data.gunning_fog_index}</b></p>
                  <p>Gunninga "miglas" klase: <b>{data.gunning_fog_klase}</b></p> */}
                  <p>Latviesu valodas meginajuma klase: <b>{data.lv_meginajuma_klase}</b></p>
                  <p>Latviesu valodas meginajuma aprēķins: <b>{data.lv_meginajuma_koef}</b></p>
                  <p>Vidējo komatu skaits teikumā: <b>{data.vid_komatu_skaits_teik}</b></p>
                  <p>Vidējais teikuma garums: <b>{data.vid_teikuma_gar}</b></p>
                  <p>Vidējais vārda garums: <b>{data.vid_varda_gar}</b></p>
                  <p>Vidējais zilbju garums vārdā: <b>{data.vid_zilbju_gar}</b></p>
                  </Tab>
                  <Tab eventKey="profile" title="Kvalitatīvie rādītāji">
                  <p>Teikuma uzbūve: <b>{data.teikumu_uzbuve}</b></p>
                  <p>Vienkāršo teikumu īpatsvars: <b>{data.vienkarso_teikumu_svars}</b></p>
                  <p>Tiešās runas: <b>{data.tiesas_runas}</b></p>
                  <p>Tiešās runas īpatsvars: <b>{data.tiesas_runas_svars}</b></p>                  
                  <p>Unikālie vārdi: </p>
                  {data.unikalie_vardi?.map((item, index) => (
                    <li className='zilbes' key={index}><b>{item}</b></li>
                  ))}
                  <p>Visi vārdi teikumā: </p>
                  {data.visi_vardi?.map((item, index) => (
                    <li className='zilbes' key={index}><b>{item}</b></li>
                  ))}  
                  <p>Zilbju saraksts: </p>
                  {data.zilbju_saraksts?.map((item, index) => (
                    <li className='zilbes' key={index}><b>{item}</b></li>
                  ))}
                  </Tab>
                  <Tab eventKey="contact" title="Lietotāju pieredze">
                  <p>Nosauktās entitātes: <b>{data.nosauktas_entitates}</b></p>
                  <p>Nosauktās entitātes īpatsvards: <b>{data.nosauktas_entitates_svars}</b></p>
                  <p>Unikālie vārdi: </p>
                  {data.unikalie_vardi?.map((item, index) => (
                    <li className='zilbes' key={index}><b>{item}</b></li>
                  ))}
                  <p>Reto vārdu uzskaite:</p>
                    <ul>
                      {Object.entries(data.reto_vardu_saraksts).map(([key, value]) => (
                        <li className='zilbes' key={key}>
                          <strong>{key}</strong>: 
                          <span className={value === 'RETS' ? 'red-text' : ''}> {value}</span>
                        </li>
                      ))}
                    </ul>
                  <p>Reto vārdu svars: <b>{data.reto_vardu_svars}</b></p>
                  </Tab>
                </Tabs>
              </div>
            )}
            </div>
          </div>
        </div>
      </div>
  );
  }
  



export default Manual;