import json

class PresetModel:
    def __init__(self, preset_file=None):
        self.preset_file = preset_file
        self.presets = {"Genere Musicale": [], "Strumento Musicale": []}
        if preset_file:
            self.load_presets(preset_file)

    def load_presets(self, file_path):
        """Carica i preset da un file JSON."""
        with open(file_path, 'r') as file:
            self.presets = json.load(file)

    def save_presets(self, file_path=None):
        """Salva i preset in un file JSON."""
        if not file_path:
            file_path = self.preset_file
        with open(file_path, 'w') as file:
            json.dump(self.presets, file, indent=4)

    def add_preset(self, category, name):
        """Aggiunge un preset a una categoria specifica."""
        if category in self.presets and name not in self.presets[category]:
            self.presets[category].append(name)

    def remove_preset(self, category, name):
        """Rimuove un preset da una categoria specifica."""
        if category in self.presets and name in self.presets[category]:
            self.presets[category].remove(name)

    def get_presets(self, category):
        """Restituisce i preset di una categoria specifica."""
        return self.presets.get(category, [])
