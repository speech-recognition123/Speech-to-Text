import './App.css';
import React  from 'react'
import AudioUpload from './components/AudioUpload'
import AudioFileUploader from "./components/AudioRecorder";
import Home from "./components/Home";
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import imgf from './image/photo_2022-06-09_10-32-07.jpg'

import "./App.css";

import { BrowserRouter, Routes, Route } from "react-router-dom";


function App() {


return (

  <BrowserRouter>
    <div className='app'>
      <div className='img'>
        <img src= {imgf}/>
      </div>
      <div className='main'>

      <Routes>
                <Route path ='/' element = {<Home/>}/>     
                <Route path ='/audio-uploader' element = {<AudioUpload/>}/>
                <Route path ='/audio-recorder' element = {<AudioFileUploader/>}/>
               
      </Routes>
    </div>

        {/* <AudioUpload />

        <AudioFileUploader/> */}
    </div>
  </BrowserRouter>
   
  );
};

export default App;
