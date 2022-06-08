import './App.css';
import React, { useState }  from 'react'
import AudioUpload from './AudioUpload'
import AudioFileUploader from "./components/AudioRecorder";
import axios from 'axios';

import "./App.css";

import { Link } from "react-router-dom";

let gumStream = null;
let recorder = null;
let audioContext = null;


function App() {
//   const startRecording = () => {
//   let constraints = {
//     audio: true,
//     video: false
// }

// audioContext = new window.AudioContext();
// console.log("sample rate: " + audioContext.sampleRate);

// navigator.mediaDevices
//     .getUserMedia(constraints)
//     .then(function (stream) {
//         console.log("initializing Recorder.js ...");

//         gumStream = stream;

//         let input = audioContext.createMediaStreamSource(stream);

//         recorder = new window.Recorder(input, {
//             numChannels: 1
//         })

//         recorder.record();
//         console.log("Recording started");
//     }).catch(function (err) {
//         //enable the record button if getUserMedia() fails
// });

// }


// const stopRecording = () => {
// console.log("stopButton clicked");

// recorder.stop(); //stop microphone access
// gumStream.getAudioTracks()[0].stop();

// recorder.exportWAV(onStop);
// }

// const onStop = (blob) => {
// console.log("uploading...");

// let data = new FormData();

// data.append('text', "this is the transcription of the audio file");
// data.append('wavfile', blob, "recording.wav");

// const config = {
//     headers: {'content-type': 'multipart/form-data'}
// }
// axios.post('http://localhost:8080/asr/', data, config);
// }

return (

<>
    <div className="App">
      <AudioUpload />
      <AudioFileUploader/>
    {/* </div>

      <div className='app'>
        <button onClick={startRecording} type="button">Start</button>
        <button onClick={stopRecording} type="button">Stop</button>
      </div> */}

    </>
  );
};


export default App;
