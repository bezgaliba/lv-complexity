import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Manual from './manual.jsx';
import ML from './ml.jsx';
import NotFound from './notfound.jsx';

import { Link } from "react-router-dom";

function Home() {
  return (
      <div>
        <div className="wrapper">
          <div className="side left">
            <div className='side image manual'></div>
            <div className='caption'>
              <h1>Manuālā</h1>
              <Link to="/manual" className='button'>Nosaki teksta sarežģītību</Link>
            </div>
          </div>
          <div className="side right">
            <div className='side image ml'></div>
            <div className='caption'>
              <h1>Mašīnmācīšanas</h1>
              <Link to="/ml" className='button'>Nosaki teksta sarežģītību</Link>
            </div>
          </div>
        </div>
        <div className='wrapperBottom'>
          <div className="side bottom">
            <div className='side image bg'></div>
            <div className='caption'>
              <a href="https://github.com/bezgaliba/lv-complexity" className='button'>Biežāk uzdotie jautājumi & apraksts</a>
            </div>
          </div>
        </div>
      </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/manual" element={<Manual />} />
        <Route path="/ml" element={<ML />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
