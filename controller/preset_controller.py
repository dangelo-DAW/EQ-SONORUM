import json
import os
class PresetController:
    def __init__(self, preset_model, ui_manager):
        self.preset_model = preset_model
        self.ui_manager = ui_manager
        self.preset_file = "presets.json" 
        self.load_presets_from_json()

    def get_presets(self, category):
        return self.preset_model.get_presets(category)

    def add_preset(self, name, category, settings):
        self.preset_model.add_preset(name, category, settings)
        self.save_presets_to_json()
        
    def save_presets_to_json(self):
        data = [
            {
                "name": preset["name"],
                "category": preset["category"],
                "settings": preset["settings"]
            }
            for category in self.preset_model.presets.values()
            for preset in category
        ]
        with open(self.preset_file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def load_presets_from_json(self):
        if os.path.exists(self.preset_file):
            with open(self.preset_file, 'r') as file:
                data = json.load(file)
                if isinstance(data, list):  # Verifica che sia una lista di preset
                    for preset in data:
                        self.preset_model.add_preset(preset["name"], preset["category"], preset["settings"])
                else:
                    raise ValueError("Formato JSON non valido: atteso un array di preset.")

    def remove_preset(self, category, name):
        self.preset_model.remove_preset(category, name)

    def apply_preset(self, preset_name):
        preset = self.preset_model.get_preset_by_name(preset_name)
        if preset:
            self.ui_manager.update_interface_with_preset(preset)
        else:
            print(f"Errore: Preset '{preset_name}' non trovato.")
            
    def rename_preset(self, old_name, new_name):
        preset = self.preset_model.get_preset_by_name(old_name)
        if preset:
            preset["name"] = new_name
            self.save_presets_to_json()

