# controllers/file_controller.py

class FileController:
    def __init__(self, audio_processor_model, view):
        self.audio_processor_model = audio_processor_model
        self.view = view

    def load_file(self, file_path):
        try:
            # Assicurati che `file_path` sia passato correttamente qui
            self.audio_processor_model.load_audio(file_path)
            self.view.update_audio_view(file_path)
            self.view.mark_as_unmodified()
        except Exception as e:
            self.view.show_error(f"Errore durante il caricamento del file: {str(e)}")

    def save_file(self, file_path):
        """
        Salva il file audio tramite l'AudioProcessor e aggiorna la UI.
        """
        try:
            # Usa il metodo export_audio per salvare il file
            self.audio_processor_model.export_audio(file_path)
            self.view.show_message(f"File salvato con successo in {file_path}.")
        except Exception as e:
            self.view.show_error(f"Errore durante il salvataggio del file: {str(e)}")


    def export_file(self, file_path, format):
        try:
            self.audio_processor_model.export_audio(file_path, format)
            self.view.show_message(f"File esportato con successo in {file_path}")
        except Exception as e:
            self.view.show_error(f"Errore durante l'esportazione: {str(e)}")
