import React from "react";
import { Button } from "./Button.js";
import "./SpeechRecog.css";

function SpeechRecog() {
    return (
        <div className="speech-container">
            <img src="/images/photo_2022-06-09_10-32-07.jpg" alt="" />
            <h1>Speech Recognition</h1>
            <p>Do you want to Upload an audio or Record a voice?</p>
            <div className="hero-btns">
                <Button
                    className="btns"
                    buttonStyle="btn--outline"
                    buttonSize="btn--large"
                    linkTo="/audio-uploader"
                >
                    Upload Audio
                </Button>
                <Button
                    className="btns"
                    buttonStyle="btn--primary"
                    buttonSize="btn--large"
                    linkTo="/audio-recorder"
                >
                    Record Voice <i className="far fa-play-circle" />
                </Button>
            </div>
        </div>
    );
}

export default SpeechRecog;
