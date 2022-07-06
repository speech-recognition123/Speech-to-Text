import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import "../node_modules/bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import AudioFileUploader from "./components/AudioRecorder";
import AudioUpload from "./components/AudioUpload";
import Home from "./components/Home";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/audio-uploader" element={<AudioUpload />} />
                <Route path="/audio-recorder" element={<AudioFileUploader />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
