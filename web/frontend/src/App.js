import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="app">
       
          <p className='p-mic'>Microphone: {Listening ? "NO" :"OFF"}</p>
            <div className='button'>
            <button onClick={startRecording} type="button">Start</button>
            <button onClick={stopRecording} type="button">Stop</button>
        </div>
        <div className="p-transcription"> 
        Text desplayed here
        </div>
        </div>
  
  );
}

export default App;
