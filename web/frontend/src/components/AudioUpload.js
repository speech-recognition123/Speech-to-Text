import React from 'react'
import axios from 'axios';
import '../../node_modules/bootstrap/dist/css/bootstrap.min.css';
import imgf from '../image/photo_2022-06-09_10-32-07.jpg'
 
class FileUpload extends React.Component{
 
    constructor(){
        super();
        this.state = {
            selectedFile:'',
        }
 
        this.handleInputChange = this.handleInputChange.bind(this);
    }
 
    handleInputChange(event) {
        this.setState({
            selectedFile: event.target.files[0],
          })
    }
 // Connect here
    submit(){
        const data = new FormData() 
        data.append('file', this.state.selectedFile)
        console.warn(this.state.selectedFile);
        let url = "http://";
 
        axios.post(url, data, { // receive two parameter endpoint url ,form data 
        })
        .then(res => { // then print response status
            console.warn(res);
        })
 
    }
    render(){
        return(


            <div className='app'>
            <div className='img'>
                 <img src= {imgf}/>
            </div>
                <div   className='main'>
                    <div >
                        <br /><br />
 
                            <h1 className="text-white">Here you can upload an audio file</h1>
                            <br />
                            <div className="form-row">
                                <div className="form-group col-md-6">
                                    <p className="text-white">Select an Audio File :</p>
                                    <pre/>
                                    <input type="file" className="form-control" name="upload_file" onChange={this.handleInputChange} />
                                </div>
                            </div>
 
                            <div className="form-row">
                                <div className="col-md-6">
                                    <button type="submit" className="btn btn-dark" onClick={()=>this.submit()}>Transcribe</button>
                                </div>
                            </div>
                    </div>
                </div>
            </div>
        )  
    }
}
 
export default FileUpload;