# data preset

class PresetController:
    def __init__(self, preset_model, ui_manager):
        """
        Inizializza il PresetController con il modello dei preset e il gestore dell'interfaccia utente.
        :param preset_model: Istanza di PresetModel che gestisce i preset.
        :param ui_manager: Istanza di UIManager che gestisce l'interfaccia utente.
        """
        self.preset_model = preset_model
        self.ui_manager = ui_manager

    def load_presets(self, file_path):
        """
        Carica i preset da un file JSON e aggiorna l'interfaccia utente.
        :param file_path: Il percorso del file JSON contenente i preset.
        """
        self.preset_model.load_presets(file_path)
        self.ui_manager.populate_preset_lists()

    def save_presets(self, file_path):
        """
        Salva i preset in un file JSON.
        :param file_path: Il percorso del file JSON in cui salvare i preset.
        """
        self.preset_model.save_presets(file_path)

    def add_preset(self, category, name):
        """
        Aggiunge un nuovo preset alla categoria specificata.
        :param category: La categoria del preset (es. "Genere Musicale", "Strumento Musicale").
        :param name: Il nome del preset da aggiungere.
        """
        self.preset_model.add_preset(category, name)
        self.ui_manager.populate_preset_lists()

    def remove_preset(self, category, name):
        """
        Rimuove un preset dalla categoria specificata.
        :param category: La categoria del preset (es. "Genere Musicale", "Strumento Musicale").
        :param name: Il nome del preset da rimuovere.
        """
        self.preset_model.remove_preset(category, name)
        self.ui_manager.populate_preset_lists()
