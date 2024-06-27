from models.file import AudioFile
from models.equalizer import Equalizer

def main():
    audio = AudioFile("path/to/your/audiofile.wav")
    audio.load_file()
    
    eq = Equalizer()
    eq.add_band(1000, 1.5, 100)
    eq.add_band(5000, 0.8, 1000)
    
    equalized_data = eq.apply_equalization(audio.data, audio.sample_rate)
    audio.data = equalized_data
    audio.save_file("path/to/equalized/audiofile.wav")

if __name__ == "__main__":
    main()
