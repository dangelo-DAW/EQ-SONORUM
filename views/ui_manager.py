from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QMessageBox, QAction, QVBoxLayout, QSplitter, QWidget, QStatusBar,
                             QPushButton, QHBoxLayout, QSlider, QLabel, QComboBox, QListWidget, QGroupBox)
from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtGui import QIcon, QPainter, QPixmap
from .slider_area import SliderArea
from .music_player import MusicPlayer
from .preset_manager import PresetManager
from controller.preset_controller import PresetController
from controller.file_controller import FileController
from models.audio_processor import AudioProcessor 
from models.preset_model import PresetModel

class UIManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.watermark = QPixmap('/home/claudio/Scrivania/EQ-SONORUM/views/images/noisy.png')  # Modifica con il percorso corretto dell'immagine di filigrana
        self.applyStyleSheet('views/style.qss')

        self.__currentFilePath = None  # Mantiene traccia del percorso del file corrente
        self.__isModified = False  # Mantiene traccia se ci sono modifiche non salvate

        self.setWindowTitle("EQ SONORUM")
        self.setGeometry(100, 100, 1200, 800)

        self.file_controller = FileController(AudioProcessor(), self)
        self.__musicPlayer = MusicPlayer()
        self.__sliderArea = SliderArea()
        self.preset_model = PresetModel()
        self.preset_controller = PresetController(self.preset_model, self)
        self.preset_manager = PresetManager(self.preset_controller, self)
        
        # Configurazione layout principale
        mainLayout = QVBoxLayout()
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.__sliderArea)
        splitter.addWidget(self.preset_manager)
        
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
        
        
    def open_preset_manager(self):
        self.preset_manager.exec_()

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

    def loadFile(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Carica File", "", "Audio Files (*.wav *.mp3 *.flac)", options=options)
        if filePath:
            self.__currentFilePath = filePath
            self.file_controller.load_file(filePath)
            fileTitle = QFileInfo(filePath).fileName()  # Ottieni il nome del file
            self.__musicPlayer.set_title(fileTitle)  # Imposta il titolo nel player
            self.__musicPlayer.play_file(filePath)
            self.__isModified = False  # Reset delle modifiche poiché è stato caricato un nuovo file

    def saveFile(self):
        if self.__currentFilePath:
            self.file_controller.save_file(self.__currentFilePath)
        else:
            self.saveFileAs()

    def saveFileAs(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getSaveFileName(self, "Salva File", "", "Audio Files (*.wav *.mp3 *.flac)", options=options)
        if filePath:
            self.__currentFilePath = filePath
            self.file_controller.save_file(filePath)
            
    def showExportDialog(self):
        if not self.__currentFilePath:
            QMessageBox.warning(self, "Errore", "Nessun file caricato.")
            return

        format_combo = QComboBox(self)
        format_combo.addItems(["mp3", "wav", "flac"])
        output_format = format_combo.currentText()
        output_file, _ = QFileDialog.getSaveFileName(self, "Salva File", "", f"*.{output_format}")

        if output_file:
            if not output_file.endswith(f".{output_format}"):
                output_file += f".{output_format}"
            self.file_controller.export_file(output_file, output_format)

    def resetAll(self):
        self.__sliderArea.reset()
        self.__currentFilePath = None
        self.__isModified = False

    def changeVolume(self, value):
        self.__musicPlayer.setVolume(value)  # Modificato da setVolume a set_volume
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
    
    def update_audio_view(self, file_path):
        fileTitle = QFileInfo(file_path).fileName()
        self.__musicPlayer.set_title(fileTitle)
        self.__musicPlayer.play_file(file_path)

    def mark_as_unmodified(self):
        self.__isModified = False

    def show_message(self, message):
        QMessageBox.information(self, "Messaggio", message)
            
    def show_error(self, error_message):
        QMessageBox.critical(self, "Errore", error_message)
        
    def updateUI(self, gain, slider_values, quality_factors):
        self.__musicPlayer.setGain(gain)
        self.__sliderArea.setSliderValues(slider_values)
        self.__sliderArea.setQualityFactor(quality_factors)
        
    def get_current_settings(self):
        """
        Raccoglie i valori attuali dei controlli dell'interfaccia e li restituisce come dizionario.
        """
        settings = {
            "gain": self.get_gain_value(),
            "slider_bands": self.get_slider_band_values(),
            "quality_factors": self.get_quality_factors()
        }

        return settings

    def update_interface_with_preset(self, preset):
        # Aggiorna i controlli dell'interfaccia con i valori del preset
        self.__sliderArea.set_gain(preset["settings"]["gain"])
        self.__sliderArea.set_slider_band_values(preset["settings"]["slider_bands"])
        self.__sliderArea.set_quality_factors(preset["settings"]["quality_factors"])

