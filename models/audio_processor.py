from pydub import AudioSegment

class AudioProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.audio = AudioSegment.from_file(file_path)
    
    def export_audio(self, output_path, format='mp3'):
        """
        Esporta l'audio nel formato specificato.
        :param output_path: Il percorso completo di output.
        :param format: Il formato di esportazione ('mp3', 'wav', 'flac').
        """
        if format not in ['mp3', 'wav', 'flac']:
            raise ValueError("Formato non supportato. Scegli tra 'mp3', 'wav', o 'flac'.")
        
        self.audio.export(output_path, format=format)
        print(f"File esportato con successo in {output_path}.")

# Esempio di utilizzo
if __name__ == "__main__":
    processor = AudioProcessor("path/to/your/file.mp3")
    processor.export_audio("path/to/exported/file.wav", format="wav")
