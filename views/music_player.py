from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class MusicPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__is_playing = False
        self.__timer = QTimer(self)
        self.__timer.setInterval(100)
        self.__timer.timeout.connect(self.update_progress)

        # Setup QMediaPlayer for playback
        self.__media_player = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.__media_player.positionChanged.connect(self.update_progress)
        self.__media_player.durationChanged.connect(self.update_duration)

        self.init_ui()

    def init_ui(self):
        self.__title_label = QLabel("Nessun file caricato")
        self.__progress_slider = QSlider(Qt.Horizontal)
        self.__progress_slider.setRange(0, 1000)
        self.__progress_slider.sliderReleased.connect(self.seek)
        self.__progress_slider.sliderPressed.connect(self.slider_pressed)
        self.__progress_slider.sliderMoved.connect(self.slider_moved)

        self.current_time_label = QLabel("00:00")
        self.total_time_label = QLabel("00:00")

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.current_time_label)
        slider_layout.addWidget(self.__progress_slider)
        slider_layout.addWidget(self.total_time_label)

        self.play_pause_button = QPushButton()
        self.play_pause_button.setIcon(QIcon.fromTheme("media-playback-start"))
        self.play_pause_button.setFixedSize(24, 24)
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
    
        self.stop_button = QPushButton()
        self.stop_button.setIcon(QIcon.fromTheme("media-playback-stop"))
        self.stop_button.setFixedSize(24, 24)
        self.stop_button.clicked.connect(self.stop)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.play_pause_button)
        button_layout.addWidget(self.stop_button)

        layout = QVBoxLayout()
        layout.addWidget(self.__title_label)
        layout.addLayout(slider_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def play_file(self, file_path):
        media_content = QMediaContent(QUrl.fromLocalFile(file_path))
        self.__media_player.setMedia(media_content)
        self.__media_player.play()

        self.__is_playing = True
        self.play_pause_button.setIcon(QIcon.fromTheme("media-playback-pause"))
        self.__timer.start()

    def toggle_play_pause(self):
        if self.__is_playing:
            self.__media_player.pause()
            self.__is_playing = False
            self.play_pause_button.setIcon(QIcon.fromTheme("media-playback-start"))
            self.__timer.stop()
        else:
            self.__media_player.play()
            self.__is_playing = True
            self.play_pause_button.setIcon(QIcon.fromTheme("media-playback-pause"))
            self.__timer.start()

    def stop(self):
        self.__media_player.stop()
        self.__is_playing = False
        self.play_pause_button.setIcon(QIcon.fromTheme("media-playback-start"))
        self.__timer.stop()
        self.__progress_slider.setValue(0)
        self.current_time_label.setText("00:00")
        self.total_time_label.setText("00:00")

    def update_progress(self):
        duration = self.__media_player.duration()
        if duration > 0:
            current_position = self.__media_player.position()
            self.__progress_slider.setValue(int((current_position / duration) * 1000))
            self.current_time_label.setText(self.format_time(current_position))

    def update_duration(self, duration):
        self.total_time_label.setText(self.format_time(duration))

    def seek(self):
        duration = self.__media_player.duration()
        if duration > 0:
            slider_value = self.__progress_slider.value()
            position = int(slider_value / self.__progress_slider.maximum() * duration)
            self.__media_player.setPosition(position)

    def slider_pressed(self):
        self.__timer.stop()

    def slider_moved(self):
        duration = self.__media_player.duration()
        if duration > 0:
            position = (self.__progress_slider.value() / self.__progress_slider.maximum()) * duration
            self.current_time_label.setText(self.format_time(position))

    def format_time(self, ms):
        seconds = int((ms / 1000) % 60)
        minutes = int((ms / (1000 * 60)) % 60)
        return f"{minutes:02}:{seconds:02}"

    def closeEvent(self, event):
        self.__media_player.stop()
        event.accept()

    def set_title(self, title):
        """Aggiorna il titolo del brano nell'interfaccia utente."""
        self.__title_label.setText(title)

    def setVolume(self, value):
        """Imposta il volume."""
        self.__media_player.setVolume(value)
