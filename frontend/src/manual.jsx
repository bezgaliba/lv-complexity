import './manual.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState } from 'react';
import { Link } from "react-router-dom";
import axios from 'axios';

function Manual() {
  const [data, setData] = useState([]);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false); 
  const [loadingScreen, setLoadingScreen] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoadingScreen(true)
      const response = await axios.get(`https://sarezgitiba-flask-yhf42gzwra-lm.a.run.app/?text=${text}`);
      const data = response.data;
      setData(data);
      setLoading(true);
      setLoadingScreen(false);
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      { loadingScreen && (
      <div className="spinner-container">
        <div className="spinner"></div>
      </div>
      )};
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
            {loading && (
              <div>
                <p>Dots teksts: <b>{data.teksts}</b></p>
                <p>Fleša-Kincaida lasīšanas viegluma klase: <b>{data.flesch_klase}</b></p>
                <p>Fleša-Kincaida lasīšanas viegluma aprēķins: <b>{data.flesch_koef}</b></p>
                <p>Gunninga "miglas" indekss: <b>{data.gunning_fog_index}</b></p>
                <p>Gunninga "miglas" klase: <b>{data.gunning_fog_klase}</b></p>
                <p>Latviesu valodas meginajuma klase: <b>{data.lv_meginajuma_klase}</b></p>
                <p>Latviesu valodas meginajuma aprēķins: <b>{data.lv_meginajuma_koef}</b></p>
                <p>Nosauktās entitātes: <b>{data.nosauktas_entitates}</b></p>
                <p>Nosauktās entitātes īpatsvards: <b>{data.nosauktas_entitates_svars}</b></p>
                <p>Reto vārdu svars: <b>{data.reto_vardu_svars}</b></p>
                <p>Teikuma uzbūve: <b>{data.teikumu_uzbuve}</b></p>
                <p>Tiešās runas: <b>{data.tiesas_runas}</b></p>
                <p>Tiešās runas īpatsvars: <b>{data.tiesas_runas_svars}</b></p>
                <p>Unikālie vārdi: <b>{data.unikalie_vardi}</b></p>
                <p>Unikālo vārdu īpatsvars: <b>{data.unikalo_vardu_svars}</b></p>
                <p>Vidējo komatu skaits teikumā: <b>{data.vid_komatu_skaits_teik}</b></p>
                <p>Vidējais teikuma garums: <b>{data.vid_teikuma_gar}</b></p>
                <p>Vidējais vārda garums: <b>{data.vid_varda_gar}</b></p>
                <p>Vidējais zilbju garums vārdā: <b>{data.vid_zilbju_gar}</b></p>
                <p>Vienkāršo teikumu īpatsvars: <b>{data.vienkarso_teikumu_svars}</b></p>
                <p>Visi vārdi teikumā: <b>{data.visi_vardi}</b></p>
                <br></br>
                <p>Zilbju saraksts: </p>
                {data.zilbju_saraksts?.map((item, index) => (
                  <p key={index}><b>{item}</b></p>
                ))}
              </div>
            )}
            </div>
          </div>
        </div>
      </div>
  );
  }
  



export default Manual;