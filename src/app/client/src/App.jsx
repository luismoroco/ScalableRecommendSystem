import { useState } from 'react';
import './App.css'

function App() {
  const API_URL = 'https://api.themoviedb.org/3';
  const API_KEY = '9a66bdb36b3a53314033a1dee8587b89';
  const AMG_PATH = 'https://image.tmdb.org/t/p/original';
  const URL_IMG = 'https://image.tmdb.org/t/p/original';

  const [movies, setMovies] = useState([]);
  const [searchKey, setSearchKey] = useState('');

  const fetchMov = async ()

  return (
    <>
      <h1> HOLA </h1>
    </>
  )
}

export default App
