from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QPushButton, QHBoxLayout, QShortcut
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QKeySequence

class MusicPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initUi()
        self.__isPlaying = False  # Stato di riproduzione iniziale
        self.__timer = QTimer(self)  # Inizializza il QTimer
        self.__timer.setInterval(100)  # Aggiorna più frequentemente per scorrimento più fluido
        self.__timer.timeout.connect(self.updateProgress)  # Collega il timer all'aggiornamento della barra di avanzamento
        
    def setVolume(self, value):
        self.__mediaPlayer.setVolume(value)

    def __initUi(self):
        self.__titleLabel = QLabel("Nessun file caricato")
        self.__mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.__progressSlider = QSlider(Qt.Horizontal)
        self.__progressSlider.setRange(0, 1000)  # Aumenta il range per una maggiore precisione
        self.__progressSlider.sliderReleased.connect(self.seek)
        self.__progressSlider.sliderPressed.connect(self.sliderPressed)
        self.__progressSlider.sliderMoved.connect(self.sliderMoved)

        # Etichette per il tempo di riproduzione
        self.currentTimeLabel = QLabel("00:00")
        self.totalTimeLabel = QLabel("00:00")

        # Creazione dei pulsanti con icone ridimensionati
        self.playPauseButton = QPushButton()
        self.playPauseButton.setIcon(QIcon.fromTheme("media-playback-start"))  # Icona play
        self.playPauseButton.setFixedSize(24, 24)  # Ridimensiona il pulsante
        self.playPauseButton.clicked.connect(self.togglePlayPause)
        
        self.stopButton = QPushButton()
        self.stopButton.setIcon(QIcon.fromTheme("media-playback-stop"))  # Icona stop
        self.stopButton.setFixedSize(24, 24)  # Ridimensiona il pulsante
        self.stopButton.clicked.connect(self.stop)

        # Scorciatoia da tastiera per il pulsante di stop
        stopShortcut = QShortcut(QKeySequence("S"), self)
        stopShortcut.activated.connect(self.stop)

        # Layout per lo slider e le etichette del tempo
        sliderLayout = QHBoxLayout()
        sliderLayout.addWidget(self.currentTimeLabel)
        sliderLayout.addWidget(self.__progressSlider)
        sliderLayout.addWidget(self.totalTimeLabel)

        # Layout per i pulsanti sotto lo slider
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.playPauseButton)
        buttonLayout.addWidget(self.stopButton)

        layout = QVBoxLayout()
        layout.addWidget(self.__titleLabel)
        layout.addLayout(sliderLayout)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

    def setTitle(self, title):
        self.__titleLabel.setText(title)

    def playFile(self, filePath):
        self.__mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filePath)))
        self.__mediaPlayer.play()
        self.__isPlaying = True
        self.playPauseButton.setIcon(QIcon.fromTheme("media-playback-pause"))  # Cambia l'icona a pausa
        self.__timer.start()

    def togglePlayPause(self):
        if self.__isPlaying:
            self.__mediaPlayer.pause()
            self.__isPlaying = False
            self.playPauseButton.setIcon(QIcon.fromTheme("media-playback-start"))  # Cambia l'icona a play
            self.__timer.stop()
        else:
            self.__mediaPlayer.play()
            self.__isPlaying = True
            self.playPauseButton.setIcon(QIcon.fromTheme("media-playback-pause"))  # Cambia l'icona a pausa
            self.__timer.start()

    def stop(self):
        self.__mediaPlayer.stop()
        self.__isPlaying = False
        self.playPauseButton.setIcon(QIcon.fromTheme("media-playback-start"))  # Cambia l'icona a play
        self.__timer.stop()
        self.__progressSlider.setValue(0)  # Riporta la barra di avanzamento a 0
        self.currentTimeLabel.setText("00:00")

    def seek(self):
        duration = self.__mediaPlayer.duration()
    
        if duration > 0:
            slider_value = self.__progressSlider.value()
            position = int(slider_value / self.__progressSlider.maximum() * duration)
        
            self.__mediaPlayer.setPosition(position)
            self.__mediaPlayer.play()

            # Riavvia il timer per continuare l'aggiornamento dello slider
        self.__timer.start()
        
    def sliderPressed(self):
        # Ferma l'aggiornamento del timer mentre l'utente sta spostando lo slider
        self.__timer.stop()

    def sliderMoved(self):
        duration = self.__mediaPlayer.duration()
    
        if duration > 0:
            slider_value = self.__progressSlider.value()
            position = int(slider_value / self.__progressSlider.maximum() * duration)
            self.currentTimeLabel.setText(self.formatTime(position))

    def updateProgress(self):
        duration = self.__mediaPlayer.duration()
        if duration > 0:
            currentPosition = self.__mediaPlayer.position()
            self.__progressSlider.setValue(int((currentPosition / duration) * 1000))
            self.currentTimeLabel.setText(self.formatTime(currentPosition))
            self.totalTimeLabel.setText(self.formatTime(duration))

    def formatTime(self, ms):
        seconds = (ms / 1000) % 60
        minutes = (ms / (1000 * 60)) % 60
        return f"{int(minutes):02}:{int(seconds):02}"

    def getVolume(self):
        return self.__mediaPlayer.volume()