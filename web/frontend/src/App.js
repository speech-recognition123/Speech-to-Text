import './App.css';
import React, { useState }  from 'react'
import AudioUpload from './components/AudioUpload'
import AudioFileUploader from "./components/AudioRecorder";
import axios from 'axios';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';

import "./App.css";

import { Link } from "react-router-dom";

let gumStream = null;
let recorder = null;
let audioContext = null;


function App() {


return (

    <>
      <div className='App'>
        <AudioUpload />

        <AudioFileUploader/>
      </div>

    </>
  );
};


export default App;
