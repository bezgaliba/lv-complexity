import './notfound.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function NotFound() {
  return (
  <div class="container">
    <div className='notimage'></div>
    <div className='notcaption'>
      <h1>401: Neeksistē</h1>
      <h1>Šī lapa nav pieejama. Atgriezieties atpakaļ</h1>
    </div>
  </div>
  );
}

export default NotFound;
