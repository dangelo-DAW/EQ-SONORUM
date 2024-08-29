from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QGroupBox, QMessageBox, QDialog, QFormLayout, QLineEdit, QComboBox, QSizePolicy, QDialogButtonBox, QInputDialog

class PresetManager(QWidget):
    def __init__(self, preset_controller, ui_manager, parent=None):
        super().__init__(parent)
        self.preset_controller = preset_controller
        self.ui_manager = ui_manager  # riferimento all'UIManager per accedere ai valori attuali
        
        # Inizializzazione dell'interfaccia utente
        self.init_ui()
        
    def init_ui(self):
        # Layout principale verticale
        main_layout = QVBoxLayout(self)
        
        # Creazione del gruppo per i preset di generi musicali
        genre_group = QGroupBox("Generi Musicali", self)
        self.genre_preset_list = QListWidget(self)
        genre_group_layout = QVBoxLayout()
        genre_group_layout.addWidget(self.genre_preset_list)
        genre_group.setLayout(genre_group_layout)
        main_layout.addWidget(genre_group)

        # Creazione del gruppo per i preset di strumenti musicali
        instrument_group = QGroupBox("Strumenti Musicali", self)
        self.instrument_preset_list = QListWidget(self)
        instrument_group_layout = QVBoxLayout()
        instrument_group_layout.addWidget(self.instrument_preset_list)
        instrument_group.setLayout(instrument_group_layout)
        main_layout.addWidget(instrument_group)

        # Imposta la stessa dimensione per entrambi i gruppi
        genre_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        instrument_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        genre_group.setFixedSize(250, 190)
        instrument_group.setFixedSize(250, 190)
        
        # Pulsante per creare un nuovo preset
        create_preset_button = QPushButton("Nuovo Preset", self)
        create_preset_button.setFixedSize(250, 30)
        main_layout.addWidget(create_preset_button)
        
        # Pulsante per rinominare un preset
        rename_preset_button = QPushButton("Rinomina Preset", self)
        rename_preset_button.setFixedSize(250, 30)
        main_layout.addWidget(rename_preset_button)
        
        # Pulsante per eliminare il preset selezionato
        delete_preset_button = QPushButton("Elimina Preset", self)
        delete_preset_button.setFixedSize(250, 30)
        main_layout.addWidget(delete_preset_button)
        
        # Connessione dei pulsanti ai metodi
        create_preset_button.clicked.connect(self.create_preset)
        rename_preset_button.clicked.connect(self.rename_preset)
        delete_preset_button.clicked.connect(self.delete_preset)
        
        self.setLayout(main_layout)
        self.populate_preset_lists()  # Popola le liste dei preset inizialmente
        
        self.genre_preset_list.itemDoubleClicked.connect(self.apply_selected_preset)
        self.instrument_preset_list.itemDoubleClicked.connect(self.apply_selected_preset)

        # Collegare i segnali di selezione
        self.genre_preset_list.itemSelectionChanged.connect(self.on_genre_selection)
        self.instrument_preset_list.itemSelectionChanged.connect(self.on_instrument_selection)
        
    def on_genre_selection(self):
        """Deseleziona i preset negli strumenti musicali quando si seleziona un genere musicale."""
        if self.genre_preset_list.selectedItems():
            self.instrument_preset_list.clearSelection()

    def on_instrument_selection(self):
        """Deseleziona i preset nei generi musicali quando si seleziona uno strumento musicale."""
        if self.instrument_preset_list.selectedItems():
            self.genre_preset_list.clearSelection()
        
    def populate_preset_lists(self):
        """Popola le liste dei preset dal controller."""
        self.genre_preset_list.clear()
        self.instrument_preset_list.clear()

        for preset in self.preset_controller.get_presets("Genere Musicale"):
            self.genre_preset_list.addItem(preset)

        for preset in self.preset_controller.get_presets("Strumento Musicale"):
            self.instrument_preset_list.addItem(preset)

    def create_preset(self):
        # Creazione di un dialogo per raccogliere nome e categoria del preset
        dialog = QDialog(self)
        dialog.setWindowTitle("Nuovo Preset")
    
        # Layout del dialogo
        layout = QFormLayout(dialog)
    
        # Campo di input per il nome del preset
        name_input = QLineEdit(dialog)
    
        # Drpdown per selezionare la categoria del preset
        category_input = QComboBox(dialog)
        category_input.addItems(["Genere Musicale", "Strumento Musicale"])

        layout.addRow("Nome Preset:", name_input)
        layout.addRow("Categoria:", category_input)

        # Aggiunta dei pulsanti Ok e Cancel
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
    
        dialog.setLayout(layout)
    
        # Esecuzione del dialogo e gestione del risultato
        if dialog.exec_() == QDialog.Accepted:
            name = name_input.text()
            category = category_input.currentText()
        
            if name:  # Controlla che il nome non sia vuoto
                # Raccogli i valori attuali dall'interfaccia utente
                settings = self.ui_manager.get_current_settings()
            
                # Salva il preset tramite il controller
                self.preset_controller.add_preset(name, category, settings)
            
                # Aggiorna le liste dei preset nella UI
                self.populate_preset_lists()
            else:
                QMessageBox.warning(self, "Errore", "Il nome del preset non può essere vuoto.")
                
    def rename_preset(self):
        """Rinomina il preset selezionato."""
        current_genre_item = self.genre_preset_list.currentItem()
        current_instrument_item = self.instrument_preset_list.currentItem()

        if current_genre_item:
            old_name = current_genre_item.text()
        elif current_instrument_item:
            old_name = current_instrument_item.text()
        else:
            QMessageBox.warning(self, "Errore", "Seleziona un preset da rinominare.")
            return

        new_name, ok = QInputDialog.getText(self, "Rinomina Preset", f"Rinomina '{old_name}' in:")
        if ok and new_name:
            self.preset_controller.rename_preset(old_name, new_name)
            self.populate_preset_lists()

    def delete_preset(self):
        """Elimina il preset selezionato dalla lista."""
        current_genre_item = self.genre_preset_list.currentItem()
        current_instrument_item = self.instrument_preset_list.currentItem()

        if current_genre_item:
            self.preset_controller.remove_preset("Genere Musicale", current_genre_item.text())
        elif current_instrument_item:
            self.preset_controller.remove_preset("Strumento Musicale", current_instrument_item.text())
        else:
            QMessageBox.warning(self, "Errore", "Seleziona un preset valido da eliminare.")

        self.populate_preset_lists()
        
    def apply_preset(self):
        """Applica il preset selezionato con il doppio clic."""
        current_genre_item = self.genre_preset_list.currentItem()
        current_instrument_item = self.instrument_preset_list.currentItem()

        if current_genre_item:
            preset_name = current_genre_item.text()
            self.preset_controller.apply_preset("Genere Musicale", preset_name)
        elif current_instrument_item:
            preset_name = current_instrument_item.text()
            self.preset_controller.apply_preset("Strumento Musicale", preset_name)

    def apply_selected_preset(self, item):
        preset_name = item.text()
        self.preset_controller.apply_preset(preset_name)