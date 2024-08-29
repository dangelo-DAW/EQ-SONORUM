import json
import os

class PresetModel:
    def __init__(self):
        self.presets = {
            "Genere Musicale": [],
            "Strumento Musicale": []
        }

    def add_preset(self, name, category, settings):
       # Aggiunge un preset alla lista appropriata in base alla categoria
        preset = {  "name": name,
                    "category": category,
                    "settings": settings,
                }
        self.presets[category].append(preset)

    def remove_preset(self, category, name):
        self.presets[category] = [preset for preset in self.presets[category] if preset["name"] != name]

    def get_all_presets(self):
        return self.presets
    
    def get_presets(self, category):
        return [preset["name"] for preset in self.presets[category]]
    
    def get_preset_by_name(self, name):
        for category in self.presets:
            for preset in self.presets[category]:
                if preset["name"] == name:
                    return preset
        return None  # Preset non trovato
    
    def load_presets_from_json(self):
        if os.path.exists(self.preset_file):
            with open(self.preset_file, "r") as file:
                data = json.load(file)
                for preset in data:
                    self.preset_model.add_preset(preset["name"], preset["category"], preset["settings"])
