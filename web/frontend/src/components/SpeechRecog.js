import React from 'react';
import '../App.css';
import { Button } from './Button';
import './SpeechRecog.css';

function SpeechRecog() {
  return (
    <div className='hero-container'>
      <video src='./images/photo_2022-06-09_10-32-07.jpg'/>
      <h1>Speech Recognition</h1>
      <p>Do you want to Upload an audio or Record a voice?</p>
      <div className='hero-btns'>
        <Button
          className='btns'
          buttonStyle='btn--outline'
          buttonSize='btn--large'
        >
          Upload Audio
        </Button>
        <Button
          className='btns'
          buttonStyle='btn--primary'
          buttonSize='btn--large'
          onClick={console.log('hey')}
        >
         Record Voice <i className='far fa-play-circle' />
        </Button>
      </div>
    </div>
  );
}

export default SpeechRecog;