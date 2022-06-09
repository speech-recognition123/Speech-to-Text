import AudioReactRecorder, { RecordState } from "audio-react-recorder";
import axios from "axios";
import React, { useState } from "react";
import ReactAudio from "react-audio-player";
import imgf from "../image/photo_2022-06-09_10-32-07.jpg";
import "./AudioRecorder.css";
import "./component.css";

const AudioRecorder = () => {
    const [recordState, setRecordState] = useState(null);
    const [audioBlob, setAudioBlob] = useState(null);
    const [transcription, setTranscription] = useState("");

    const start = () => {
        setAudioBlob(null);
        setRecordState(RecordState.START);
    };

    const stop = () => {
        setRecordState(RecordState.STOP);
    };

    //audioData contains blob and blobUrl
    const onStop = (audioData) => {
        console.log("audioData", audioData);
        setAudioBlob(audioData);
    };

    const submit = () => {
        const data = new FormData();
        data.append("file", audioBlob["blob"]);
        let url = "http://localhost:5000/predict";

        axios.post(url, data).then((res) => {
            const { data } = res;

            setTranscription(data.data);
        });
    };

    return (
        <>
            <div className="app">
                <div className="img">
                    <img src={imgf} alt="" />
                </div>

                <div className="main">
                    <div className="container">
                        <div className="display">
                            <div className="text-center">
                                <h2>Record Audio</h2>
                                <button
                                    onClick={start}
                                    type="button"
                                    className="button"
                                >
                                    Start
                                </button>
                                <button
                                    onClick={stop}
                                    type="button"
                                    className="button"
                                >
                                    Stop
                                </button>
                            </div>
                            <div className="mt-4">
                                <AudioReactRecorder
                                    state={recordState}
                                    onStop={onStop}
                                />
                            </div>

                            {!!audioBlob && (
                                <div className="my-4">
                                    <ReactAudio
                                        src={audioBlob["url"]}
                                        controls
                                    />
                                </div>
                            )}

                            {!!audioBlob && (
                                <div className="mt-4">
                                    <div className="col-md-6">
                                        <button
                                            type="submit"
                                            className="btn btn-dark"
                                            onClick={() => submit()}
                                        >
                                            Transcribe
                                        </button>
                                    </div>
                                </div>
                            )}

                            {!!transcription && (
                                <div className="mt-4">
                                    <hr />
                                    <p>Transcription here...</p>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};
export default AudioRecorder;
