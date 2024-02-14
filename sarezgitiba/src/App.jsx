import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
  <div>
    <div className="wrapper">
        <div className="side left">
          <div className='side image manual'></div>
          <div className='caption'>
            <h1>Manuālā</h1>
            <a href='#' className='button'>Nosaki sarežģītību</a>
          </div>
      </div>
        <div className="side right">
          <div className='side image ml'></div>
          <div className='caption'>
            <h1>Mašīnmācīšanas</h1>
            <a href='#' className='button'>Nosaki sarežģītību</a>
          </div>
      </div>
    </div>
      <div className='wrapperBottom'>
      <div className="side bottom">
        <div className='side image bg'></div>
        <div className='caption'>
          <a href='#' className='button'>Biežāk uzdotie jautājumi</a>
          </div>
          </div>
    </div>
  </div>
  );
}

export default App;
