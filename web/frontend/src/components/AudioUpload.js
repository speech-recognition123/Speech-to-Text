import axios from "axios";
import React from "react";
import ReactAudio from "react-audio-player";
import "../../node_modules/bootstrap/dist/css/bootstrap.min.css";
import imgf from "../image/photo_2022-06-09_10-32-07.jpg";
import "./component.css";

class FileUpload extends React.Component {
    constructor() {
        super();
        this.state = {
            selectedFile: null,
            transcription: "",
        };

        this.handleInputChange = this.handleInputChange.bind(this);
    }

    handleInputChange(event) {
        this.setState({
            selectedFile: event.target.files[0],
        });
    }
    // Connect here
    submit() {
        const data = new FormData();
        data.append("file", this.state.selectedFile);
        console.warn(this.state.selectedFile);
        let url = "http://localhost:5000/predict";

        axios.post(url, data).then((res) => {
            const { data } = res;

            this.setState({
                transcription: data.data,
            });
        });
    }

    render() {
        return (
            <div className="app">
                <div className="img">
                    <img src={imgf} alt="" />
                </div>
                <div className="main">
                    <div>
                        <h1 className="text-white">
                            Here you can upload an audio file
                        </h1>
                        <br />
                        <div className="form-row">
                            <div className="form-group col-md-6">
                                <p className="text-white">
                                    Select an Audio File :
                                </p>
                                <input
                                    accept="audio/*"
                                    type="file"
                                    className="form-control"
                                    name="upload_file"
                                    onChange={this.handleInputChange}
                                />
                            </div>
                        </div>
                        {!!this.state.selectedFile && (
                            <div className="my-4">
                                <ReactAudio
                                    src={
                                        this.state.selectedFile &&
                                        URL.createObjectURL(
                                            this.state.selectedFile
                                        )
                                    }
                                    controls
                                />
                            </div>
                        )}
                        <div className="form-row mt-4">
                            <div className="col-md-6">
                                <button
                                    type="submit"
                                    className="btn btn-dark"
                                    onClick={() => this.submit()}
                                >
                                    Transcribe
                                </button>
                            </div>
                        </div>

                        <div className="mt-4">
                            <hr />
                            <p>Transcription here...</p>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default FileUpload;
