from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QMessageBox, QAction, QVBoxLayout, QSplitter, QWidget, QStatusBar,
                             QPushButton, QHBoxLayout, QSlider, QLabel, QComboBox, QListWidget, QListWidgetItem, 
                             QLineEdit, QInputDialog, QDialog, QFormLayout, QDialogButtonBox, QGroupBox)
from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QPalette
from slider_area import SliderArea
from music_player import MusicPlayer
from models.audio_processor import AudioProcessor  # Assicurati che il modello sia nel percorso corretto
from models.preset_model import PresetModel
from controller.preset_controller import PresetController
from models.equalizer_model import EqualizerModel

class UIManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.watermark = QPixmap('/home/claudio/Scrivania/EQ-SONORUM/views/images/noisy.png')  # Modifica con il percorso corretto dell'immagine di filigrana
        self.applyStyleSheet('style.qss')

        self.__currentFilePath = None  # Mantiene traccia del percorso del file corrente
        self.__isModified = False  # Mantiene traccia se ci sono modifiche non salvate

        self.setWindowTitle("EQ SONORUM")
        self.setGeometry(100, 100, 1200, 800)

        # Creazione del modello e del controller dell'equalizzatore
        self.equalizer_model = EqualizerModel()
        
        # Creazione del modello e del controller dei preset
        self.preset_model = PresetModel()
        self.preset_controller = PresetController(self.preset_model, self)
        
        # Creazione dei widget
        self.__musicPlayer = MusicPlayer()
        self.__sliderArea = SliderArea(self.equalizer_model)

        # Configurazione layout principale
        mainLayout = QVBoxLayout()
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.__sliderArea)

        # Sezione dei preset (sul lato destro)
        self.genre_preset_list = QListWidget(self)
        self.instrument_preset_list = QListWidget(self)
        self.populate_preset_lists()

        # Aggiungi le liste dei preset al layout con dei gruppi
        presetLayout = QVBoxLayout()

        genreGroup = QGroupBox("Generi Musicali")
        genreGroup.setFixedSize(200, 150)
        genreGroupLayout = QVBoxLayout()
        genreGroupLayout.addWidget(self.genre_preset_list)
        genreGroup.setLayout(genreGroupLayout)
        genreGroup.setStyleSheet("QGroupBox { color: white; }")  # Cambia il colore del testo a bianco
        presetLayout.addWidget(genreGroup)

        instrumentGroup = QGroupBox("Strumenti Musicali")
        instrumentGroup.setFixedSize(200, 150)
        instrumentGroupLayout = QVBoxLayout()
        instrumentGroupLayout.addWidget(self.instrument_preset_list)
        instrumentGroup.setLayout(instrumentGroupLayout)
        instrumentGroup.setStyleSheet("QGroupBox { color: white; }")  # Cambia il colore del testo a bianco
        presetLayout.addWidget(instrumentGroup)

        # Pulsanti per gestire i preset
        createPresetButton = QPushButton("New Preset")
        createPresetButton.clicked.connect(self.create_preset)
        
        deletePresetButton = QPushButton("Delete")
        deletePresetButton.clicked.connect(self.delete_preset)

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(createPresetButton)
        buttonLayout.addWidget(deletePresetButton)
        presetLayout.addLayout(buttonLayout)

        splitter.addWidget(QWidget())  # Aggiungi uno spazio tra i controlli degli slider e la sezione dei preset
        splitter.widget(1).setLayout(presetLayout)  # Aggiungi il layout dei preset allo splitter

        # Pulsante "Add File..." per caricare un brano
        addButton = QPushButton("Add File...")
        addButton.setFixedSize(100, 24)
        addButton.clicked.connect(self.loadFile)

        # Pulsante "Reset" per riportare tutti i widget allo stato iniziale
        resetButton = QPushButton("Reset")
        resetButton.setFixedSize(100, 24)
        resetButton.clicked.connect(self.resetAll)

        # Slider per il controllo del volume generale
        volumeSlider = QSlider(Qt.Horizontal)
        volumeSlider.setMinimum(0)
        volumeSlider.setMaximum(100)
        volumeSlider.setValue(50)  # Imposta il valore iniziale a 50 (metà volume)
        volumeSlider.setTickPosition(QSlider.TicksBelow)
        volumeSlider.setTickInterval(10)
        volumeSlider.setFixedSize(80, 20)  # Ridimensiona lo slider del volume
        volumeSlider.valueChanged.connect(self.changeVolume)

        # Label per mostrare il valore attuale del volume
        self.volumeLabel = QLabel("50%")
        self.volumeLabel.setFixedWidth(40)
        self.volumeLabel.setAlignment(Qt.AlignCenter)

        # Pulsante per il controllo del volume (on/off)
        volumeButton = QPushButton()
        volumeButton.setIcon(QIcon.fromTheme("audio-volume-high"))  # Icona volume alto
        volumeButton.setFixedSize(24, 24)
        volumeButton.clicked.connect(self.toggleMute)
        self.volumeButton = volumeButton  # Salva il riferimento per l'aggiornamento dell'icona

        # Layout per i pulsanti a sinistra del player
        leftControlLayout = QVBoxLayout()
        leftControlLayout.addWidget(resetButton)
        leftControlLayout.addWidget(addButton)
        leftControlLayout.addStretch()

        # Layout per il player e il controllo del volume
        playerLayout = QHBoxLayout()
        playerLayout.addLayout(leftControlLayout)  # Aggiungi i pulsanti "Add File" e "Reset" a sinistra
        playerLayout.addWidget(self.__musicPlayer)
        playerLayout.addWidget(volumeSlider)  # Aggiungi lo slider del volume
        playerLayout.addWidget(self.volumeLabel)  # Aggiungi la label per il volume
        playerLayout.addWidget(volumeButton)  # Aggiungi il pulsante di controllo del volume

        mainLayout.addWidget(splitter)
        mainLayout.addLayout(playerLayout)

        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        # Aggiunta della barra di stato
        self.setStatusBar(QStatusBar())

        # Creazione dei menu e delle azioni
        self.createMenus()

        # Configurazione del doppio clic sui preset
        self.genre_preset_list.itemDoubleClicked.connect(self.select_preset)
        self.instrument_preset_list.itemDoubleClicked.connect(self.select_preset)

    def createMenus(self):
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu("&File")

        loadAction = QAction("Load File", self)
        loadAction.triggered.connect(self.loadFile)
        fileMenu.addAction(loadAction)

        saveAction = QAction("Salva", self)
        saveAction.triggered.connect(self.saveFile)
        fileMenu.addAction(saveAction)
        
        saveAsAction = QAction("Salva con nome...", self)
        saveAsAction.triggered.connect(self.saveFileAs)
        fileMenu.addAction(saveAsAction)
        
        # Aggiunta della voce di menu per esportare il file
        exportAction = QAction('Esporta File', self)
        exportAction.triggered.connect(self.showExportDialog)
        fileMenu.addAction(exportAction)

        # Aggiungi opzioni di caricamento/salvataggio preset
        presetMenu = menuBar.addMenu("&Preset")

        loadPresetAction = QAction("Carica Preset", self)
        loadPresetAction.triggered.connect(self.load_presets)
        presetMenu.addAction(loadPresetAction)

        savePresetAction = QAction("Salva Preset", self)
        savePresetAction.triggered.connect(self.save_presets)
        presetMenu.addAction(savePresetAction)

    def loadFile(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Carica File", "", 
                                                  "Audio Files (*.wav *.mp3 *.flac)", options=options)
        if filePath:
            self.__currentFilePath = filePath
            fileTitle = QFileInfo(filePath).fileName()  # Ottieni il nome del file
            self.__musicPlayer.setTitle(fileTitle)  # Imposta il titolo nel player
            self.__musicPlayer.playFile(filePath)
            self.__isModified = False  # Reset delle modifiche poiché è stato caricato un nuovo file

    def applyEqualization(self, settings):
        self.__isModified = True  # Segna il file come modificato

    def saveFile(self):
        if self.__currentFilePath:
            self.__saveToFile(self.__currentFilePath)
        else:
            self.saveFileAs()

    def saveFileAs(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getSaveFileName(self, "Salva File", "", 
                                                  "Audio Files (*.wav *.mp3 *.flac)", options=options)
        if filePath:
            self.__saveToFile(filePath)

    def __saveToFile(self, filePath):
        try:
            self.__currentFilePath = filePath
            self.__isModified = False
            QMessageBox.information(self, "Salvato", f"File salvato con successo in {filePath}")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore durante il salvataggio del file: {str(e)}")
            
    def showExportDialog(self):
        if not self.__currentFilePath:
            QMessageBox.warning(self, "Errore", "Nessun file caricato.")
            return

        # Seleziona il formato di esportazione
        format_combo = QComboBox(self)
        format_combo.addItems(["mp3", "wav", "flac"])

        # Seleziona il percorso di salvataggio
        output_format = format_combo.currentText()
        output_file, _ = QFileDialog.getSaveFileName(self, "Salva File", "", f"*.{output_format}")

        if not output_file:
            return

        # Aggiungi estensione se non è già inclusa
        if not output_file.endswith(f".{output_format}"):
            output_file += f".{output_format}"

        try:
            # Crea l'istanza del processore e salva il file
            processor = AudioProcessor(self.__currentFilePath)
            processor.export_audio(output_file, format=output_format)
            QMessageBox.information(self, "Successo", f"File esportato con successo in {output_file}!")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore durante l'esportazione: {str(e)}")

    def resetAll(self):
        self.__sliderArea.reset()
        self.__currentFilePath = None
        self.__isModified = False

    def changeVolume(self, value):
        self.__musicPlayer.setVolume(value)
        self.volumeLabel.setText(f"{value}%")  # Aggiorna il valore del volume
        # Cambia l'icona del pulsante del volume in base al valore
        if value == 0:
            self.volumeButton.setIcon(QIcon.fromTheme("audio-volume-muted"))
        elif value <= 50:
            self.volumeButton.setIcon(QIcon.fromTheme("audio-volume-low"))
        else:
            self.volumeButton.setIcon(QIcon.fromTheme("audio-volume-high"))

    def toggleMute(self):
        currentVolume = self.__musicPlayer.getVolume()
        if currentVolume > 0:
            self.previousVolume = currentVolume  # Salva il volume attuale prima di mutare
            self.setVolumeMute()
        else:
            self.__musicPlayer.setVolume(self.previousVolume)
            self.volumeLabel.setText(f"{self.previousVolume}%")
            self.volumeButton.setIcon(QIcon.fromTheme("audio-volume-high" if self.previousVolume > 50 else "audio-volume-low"))
            # Aggiorna lo slider del volume
            volumeSlider = self.findChild(QSlider)
            volumeSlider.setValue(self.previousVolume)

    def setVolumeMute(self):
        self.__musicPlayer.setVolume(0)
        self.volumeLabel.setText("0%")  # Aggiorna la label per il volume
        self.volumeButton.setIcon(QIcon.fromTheme("audio-volume-muted"))
        # Aggiorna lo slider del volume
        volumeSlider = self.findChild(QSlider)
        volumeSlider.setValue(0)

    def closeEvent(self, event):
        if self.__isModified:
            reply = QMessageBox.question(self, "Modifiche non salvate",
                                         "Vuoi salvare le modifiche prima di uscire?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.saveFile()
                event.accept()
            elif reply == QMessageBox.Cancel:
                event.ignore()
            else:
                event.accept()
        else:
            event.accept()
            
    def applyStyleSheet(self, styleSheetFile):
        with open(styleSheetFile, "r") as file:
            self.setStyleSheet(file.read())

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Disegna la filigrana in basso a destra
        painter.setOpacity(0.05)  # Cambia l'opacità della filigrana (0.0 - 1.0)
        watermark_scaled = self.watermark.scaled(2400, 2000, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        watermark_x = self.width() - watermark_scaled.width()  # Posiziona a destra con un margine
        watermark_y = self.height() - watermark_scaled.height()   # Posiziona in basso con un margine
        painter.drawPixmap(watermark_x, watermark_y, watermark_scaled)
    
    def populate_preset_lists(self):
        """Popola le liste dei preset dall'istanza PresetModel."""
        self.genre_preset_list.clear()
        self.instrument_preset_list.clear()

        for preset in self.preset_model.get_presets("Genere Musicale"):
            self.genre_preset_list.addItem(preset)

        for preset in self.preset_model.get_presets("Strumento Musicale"):
            self.instrument_preset_list.addItem(preset)
    
    def load_presets(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Carica Preset", "", 
                                                  "Preset Files (*.json)", options=options)
        if filePath:
            self.preset_controller.load_presets(filePath)
            self.populate_preset_lists()

    def save_presets(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getSaveFileName(self, "Salva Preset", "", 
                                                  "Preset Files (*.json)", options=options)
        if filePath:
            self.preset_controller.save_presets(filePath)

    def create_preset(self):
        dialog = PresetManagerDialog(self.preset_model.presets, self)
        if dialog.exec_() == QDialog.Accepted:
            self.preset_model.presets = dialog.get_presets()
            self.populate_preset_lists()

    def delete_preset(self):
        currentGenreItem = self.genre_preset_list.currentItem()
        currentInstrumentItem = self.instrument_preset_list.currentItem()

        if currentGenreItem and currentGenreItem.text() in self.preset_model.get_presets("Genere Musicale"):
            self.preset_model.remove_preset("Genere Musicale", currentGenreItem.text())
        elif currentInstrumentItem and currentInstrumentItem.text() in self.preset_model.get_presets("Strumento Musicale"):
            self.preset_model.remove_preset("Strumento Musicale", currentInstrumentItem.text())
        else:
            QMessageBox.warning(self, "Errore", "Seleziona un preset valido da eliminare.")
            return

        self.populate_preset_lists()

    def select_preset(self):
        current_genre_item = self.genre_preset_list.currentItem()
        current_instrument_item = self.instrument_preset_list.currentItem()

        if current_genre_item:
            QMessageBox.information(self, "Preset Selezionato", f"Hai selezionato il preset: {current_genre_item.text()}")
        elif current_instrument_item:
            QMessageBox.information(self, "Preset Selezionato", f"Hai selezionato il preset: {current_instrument_item.text()}")
        else:
            QMessageBox.warning(self, "Errore", "Seleziona un preset valido.")

class PresetManagerDialog(QDialog):
    def __init__(self, presets, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestione Preset")
        self.setModal(True)
        self.presets = presets

        # Layout del form
        layout = QFormLayout()

        # Campo di input per il nome del preset
        self.presetNameInput = QLineEdit(self)
        layout.addRow("Nome Preset:", self.presetNameInput)

        # Dropdown per selezionare la categoria del preset
        self.categoryCombo = QComboBox(self)
        self.categoryCombo.addItems(["Genere Musicale", "Strumento Musicale"])
        layout.addRow("Categoria:", self.categoryCombo)

        # Pulsanti di gestione
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.save_preset)
        buttons.rejected.connect(self.reject)

        layout.addRow(buttons)
        self.setLayout(layout)

    def save_preset(self):
        name = self.presetNameInput.text().strip()
        category = self.categoryCombo.currentText()
        
        if not name:
            QMessageBox.warning(self, "Errore", "Il nome del preset non può essere vuoto.")
            return
        
        # Aggiungi o aggiorna il preset
        if name not in self.presets[category]:
            self.presets[category].append(name)
        else:
            QMessageBox.warning(self, "Errore", "Il preset esiste già.")

        self.accept()  # Chiude il dialogo con successo

    def get_presets(self):
        return self.presets
