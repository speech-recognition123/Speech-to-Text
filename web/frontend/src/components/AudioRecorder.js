
import axios from "axios";

import React, { useState } from "react";
import "./AudioRecorder.css";


let gumStream = null;
let recorder = null;
let audioContext = null;

const AudioRecorder = () => {
  

  const startRecording = () => {
    let constraints = {
      audio: true,
      video: false,
    };

    audioContext = new window.AudioContext();
    console.log("sample rate: " + audioContext.sampleRate);

    navigator.mediaDevices
      .getUserMedia(constraints)
      .then(function (stream) {
        console.log("initializing Recorder.js ...");

        gumStream = stream;

        let input = audioContext.createMediaStreamSource(stream);
        console.log(input);

        recorder = new window.Recorder(input, {
          numChannels: 1,
        });

        console.log(recorder);
        recorder.record();
        console.log("Recording started");
      })
      .catch(function (err) {
        //enable the record button if getUserMedia() fails
        console.log(err);
      });
  };

  const stopRecording = () => {
    console.log("stopButton clicked");

    recorder.stop(); //stop microphone access
    gumStream.getAudioTracks()[0].stop();

    recorder.exportWAV(onStop);
  };

  const onStop = (blob) => {
    console.log("uploading...");

    let data = new FormData();

    data.append("text", "this is the transcription of the audio file");
    data.append("wavfile", blob, "recording.wav");

    const config = {
      headers: { "content-type": "multipart/form-data" },
    };
    console.log(data);
    axios.post("http://localhost:8080/asr/", data, config);
  };

  // const [file, setFile] = useState();

  // function handleChange(event) {
  //   setFile(event.target.files[0]);
  // }

  // function handleSubmit(event) {
  //   event.preventDefault();
  //   //const url = "http://localhost:3000/uploadFile";
  //   const formData = new FormData();
  //   formData.append("file", file);
  //   formData.append("fileName", file.name);
  //   console.log(file.name);

  // }

  return (
 <>
    <div className='container'>
        <div className='display'>
            <div>
                <h2>Record Audio</h2>
                  <button onClick={startRecording} type="button">
                    Start
                  </button>
                  <button onClick={stopRecording} type="button">
                    Stop
                  </button>
                </div>
                <br></br>
                <br></br>
                <audio autoPlay controls></audio> 
      </div>
    </div>
       </>
  )
};
export  default AudioRecorder;
