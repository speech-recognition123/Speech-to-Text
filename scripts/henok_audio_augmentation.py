import librosa
import numpy as np



class AugmentAudio:
    def __init__(self) -> None:
        pass

    def add_noise(data, noise_factor):
        noise = np.random.randn(len(data))
        augmented_data = data + noise_factor * noise
        augmented_data = augmented_data.astype(type(data[0]))
        
        return augmented_data
    
