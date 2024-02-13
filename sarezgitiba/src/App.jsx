import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
  <div class="parent">
  
  <div class="item" style={{background: 'url(https://unsplash.it/800/300) center center no-repeat', backgroundSize: 'cover'}}></div>
    
    <div class="item last">
      <h2>Flexbox - Split Screen Layout</h2>
      <p>Example of a split screen layout that uses flexbox.</p>
      <p>A media query is used to detect if the virewport is below 600px, if it is then <b>flex-direction</b> is set to column-reverse, so that the image is displayed after the copy, useful on mobile devices!.</p>
      <p>Reduce the window size to below 600px to see an example.</p>
    </div>
    
  </div>
  );
}

export default App;
