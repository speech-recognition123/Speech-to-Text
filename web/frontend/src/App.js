import './App.css';
import React  from 'react'
import AudioUpload from './components/AudioUpload'
import AudioFileUploader from "./components/AudioRecorder";
import Home from "./components/Home";
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';


import { BrowserRouter, Routes, Route } from "react-router-dom";


function App() {


return (

  <BrowserRouter>
    

      <Routes>
                <Route path ='/' element = {<Home/>}/>     
                <Route path ='/audio-uploader' element = {<AudioUpload/>}/>
                <Route path ='/audio-recorder' element = {<AudioFileUploader/>}/>
               
      </Routes>

        {/* <AudioUpload />

        <AudioFileUploader/> */}
  </BrowserRouter>
   
  );
};

export default App;
