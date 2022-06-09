import './App.css';
import React  from 'react'
import AudioUpload from './components/AudioUpload'
import AudioFileUploader from "./components/AudioRecorder";
import Home from "./components/Home";
import axios from 'axios';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';

import "./App.css";

import { BrowserRouter, Routes, Route } from "react-router-dom";


function App() {


return (

  <BrowserRouter>
    <div className='App'>
    <Routes>
      <Route path ='/' element = {<Home/>}/>

        </Routes>
      <Routes>
      <Route path ='/audio-uploader' element = {<AudioUpload/>}/>

        </Routes>
        <Routes>
      <Route path ='/audio-recorder' element = {<AudioFileUploader/>}/>

        </Routes>
        {/* <AudioUpload />

        <AudioFileUploader/> */}
   
    </div>
  </BrowserRouter>
   
  );
};


export default App;
