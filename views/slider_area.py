from PyQt5.QtWidgets import QWidget, QGridLayout, QSlider, QLabel, QPushButton, QDial, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen

class SliderArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        self.sliders = []
        self.quality_dials = []
        self.lock_buttons = []
        self.mute_buttons = []

        self.create_gain_slider()

        bands = [
            ('31 Hz', 'Slider_31'), 
            ('63 Hz', 'Slider_63'), 
            ('125 Hz', 'Slider_125'), 
            ('250 Hz', 'Slider_250'), 
            ('500 Hz', 'Slider_500'), 
            ('1 kHz', 'Slider_1000'), 
            ('2 kHz', 'Slider_2000'), 
            ('4 kHz', 'Slider_4000'), 
            ('8 kHz', 'Slider_8000'), 
            ('16 kHz', 'Slider_16000')
        ]

        self.add_band_controls(bands)

    def create_gain_slider(self):
        self.gain_slider = QSlider(Qt.Vertical, self)
        self.gain_slider.setMinimum(-18)
        self.gain_slider.setMaximum(18)
        self.gain_slider.setValue(0)
        self.gain_slider.setTickPosition(QSlider.NoTicks)
        self.gain_slider.setFixedHeight(300)

        gain_value_label = QLabel("0 dB", self)
        gain_value_label.setAlignment(Qt.AlignCenter)
        self.gain_slider.valueChanged.connect(lambda value: gain_value_label.setText(f"{value} dB"))

        gain_label = QLabel("GAIN", self)
        gain_label.setAlignment(Qt.AlignCenter)

        gain_ticks_left = TickMarks(self.gain_slider, tick_interval=2)
        gain_ticks_right = TickMarks(self.gain_slider, tick_interval=2)

        gain_layout = QHBoxLayout()
        gain_layout.addWidget(gain_ticks_left)
        gain_layout.addWidget(self.gain_slider)
        gain_layout.addWidget(gain_ticks_right)

        self.layout.addLayout(gain_layout, 1, 0, Qt.AlignCenter)
        self.layout.addWidget(gain_value_label, 0, 0, Qt.AlignCenter)
        self.layout.addWidget(gain_label, 2, 0, Qt.AlignCenter)

    def add_band_controls(self, bands):
        lock_label = QLabel("Lock Band:", self)
        lock_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(lock_label, 3, 0, Qt.AlignCenter)

        quality_label = QLabel("Quality\nFactor:", self)
        quality_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(quality_label, 4, 0, Qt.AlignCenter)

        mute_label = QLabel("Mute:", self)
        mute_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(mute_label, 6, 0, Qt.AlignCenter)

        self.band_sliders = []  # Aggiunta di una lista per mantenere i riferimenti agli slider delle bande

        for i, (band, slider_name) in enumerate(bands):
            slider = QSlider(Qt.Vertical)
            slider.setMinimum(-18)
            slider.setMaximum(18)
            slider.setValue(0)
            slider.setTickPosition(QSlider.NoTicks)
            slider.setFixedHeight(300)

            value_label = QLabel("0 dB", self)
            value_label.setAlignment(Qt.AlignCenter)
            slider.valueChanged.connect(lambda value, label=value_label: label.setText(f"{value} dB"))

            label = QLabel(band, self)
            label.setAlignment(Qt.AlignCenter)

            lock_button = QPushButton("🔒", self)
            lock_button.setCheckable(True)
            lock_button.toggled.connect(lambda checked, i=i: self.toggle_lock(i, checked))

            self.lock_buttons.append(lock_button)
            self.sliders.append(slider)  # Aggiunta dello slider alla lista generale degli slider
            self.band_sliders.append(slider)  # Aggiunta alla lista specifica degli slider delle bande
            
            quality_dial = QDial(self)
            quality_dial.setMinimum(1)
            quality_dial.setMaximum(20)
            quality_dial.setValue(10)
            quality_dial.setFixedSize(50, 50)
            quality_dial.setNotchesVisible(True)

            self.quality_dials.append(quality_dial)

            quality_value_label = QLabel(f"{5.0:.1f}", self)
            quality_value_label.setAlignment(Qt.AlignCenter)
            quality_dial.valueChanged.connect(lambda value, label=quality_value_label: label.setText(f"{value / 2:.1f}"))

            mute_button = QPushButton("🔇", self)
            mute_button.setCheckable(True)
            mute_button.setStyleSheet("padding: 5px; font-size: 14px;")
            mute_button.setFixedSize(80, 25)
            
            self.mute_buttons.append(mute_button)

            tick_left = TickMarks(slider, tick_interval=2)
            tick_right = TickMarks(slider, tick_interval=2)

            slider_layout = QHBoxLayout()
            slider_layout.addWidget(tick_left)
            slider_layout.addWidget(slider)
            slider_layout.addWidget(tick_right)

            self.layout.addWidget(value_label, 0, i + 1, Qt.AlignCenter)
            self.layout.addLayout(slider_layout, 1, i + 1, Qt.AlignCenter)
            self.layout.addWidget(label, 2, i + 1, Qt.AlignCenter)
            self.layout.addWidget(lock_button, 3, i + 1, Qt.AlignCenter)
            self.layout.addWidget(quality_dial, 4, i + 1, Qt.AlignCenter)
            self.layout.addWidget(quality_value_label, 5, i + 1, Qt.AlignCenter)
            self.layout.addWidget(mute_button, 6, i + 1, Qt.AlignCenter)

    def reset(self):
        # Resetta tutti gli slider ai valori predefiniti
        for slider in self.sliders:
            slider.setValue(0)

        # Resetta il gain
        self.gain_slider.setValue(0)

        # Resetta tutti i quality dial ai valori predefiniti
        for dial in self.quality_dials:
            dial.setValue(10)

        # Resetta i pulsanti di mute e lock
        for mute_button in self.mute_buttons:
            mute_button.setChecked(False)
            mute_button.setStyleSheet("")

        for lock_button in self.lock_buttons:
            lock_button.setChecked(False)
            lock_button.setText("🔒")
            corresponding_slider = self.sliders[self.lock_buttons.index(lock_button)]
            corresponding_slider.setEnabled(True)
            
    def toggle_lock(self, band_index, checked):
        """ Blocca o sblocca la banda specificata. """
        self.lock_buttons[band_index].setText("🔓" if checked else "🔒")
        self.sliders[band_index].setEnabled(not checked)
    
    def toggle_mute(self, band_index):
        is_muted = self.mute_buttons[band_index].isChecked()
        button = self.mute_buttons[band_index]
    
        if is_muted:
            button.setStyleSheet("background-color: #28911c; color: white;")
        else:
            button.setStyleSheet("")

    def get_gain_value(self):
        return self.gain_slider.value()

    def get_quality_factors(self):
        return [dial.value() / 2 for dial in self.quality_dials]

    def get_slider_bands(self):
        return [slider.value() for slider in self.band_sliders]
    
    def set_gain(self, gain):
        self.gain_slider.setValue(gain)
    
    def set_slider_band_values(self, values):
        for i, value in enumerate(values):
            self.sliders[i].setValue(value)
    
    def set_quality_factors(self, factors):
        for i, factor in enumerate(factors):
            self.quality_dials[i].setValue(int(factor * 2))

class TickMarks(QWidget):
    def __init__(self, slider, tick_interval, parent=None):
        super().__init__(parent)
        self.slider = slider
        self.tick_interval = tick_interval
        self.setFixedWidth(10)

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.gray)
        pen.setWidth(2)
        painter.setPen(pen)

        slider_height = self.slider.height()
        num_ticks = (self.slider.maximum() - self.slider.minimum()) // self.tick_interval
        tick_spacing = slider_height / num_ticks

        for i in range(num_ticks + 1):
            y = int(i * tick_spacing)
            painter.drawLine(0, y, self.width(), y)
