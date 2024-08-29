from pydub import AudioSegment

class AudioProcessor:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.audio = None
        if file_path:
            self.load_audio(file_path)
    
    def load_audio(self, file_path):
        """
        Carica un file audio dato il percorso del file.
        :param file_path: Il percorso del file da caricare.
        """
        self.file_path = file_path
        self.audio = AudioSegment.from_file(file_path)
        print(f"File audio caricato con successo da {file_path}.")

    def export_audio(self, output_path, format='mp3'):
        """
        Esporta l'audio nel formato specificato.
        """
        if not self.audio:
            raise RuntimeError("Nessun audio caricato.")
        if format not in ['mp3', 'wav', 'flac']:
            raise ValueError("Formato non supportato. Scegli tra 'mp3', 'wav', o 'flac'.")
        
        self.audio.export(output_path, format=format)
        print(f"File esportato con successo in {output_path}.")


