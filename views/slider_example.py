import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QLabel, QGridLayout, QWidget, QSizePolicy 
from PyQt5.QtCore import Qt 

class SliderWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Equalizer Example")
        self.setGeometry(100, 100, 1200, 800)

        # Crea un widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Crea un layout griglia
        grid_layout = QGridLayout()

        # Frequenze degli slider
        frequencies = [31, 63, 125, 250, 500, 1, 2, 4, 8, 16]

        # Aggiungi molte righe per maggiore precisione
        num_rows = 100

        # Etichette del gain
        grid_layout.addWidget(QLabel("+18 dB", alignment=Qt.AlignRight), 2, 0)
        grid_layout.addWidget(QLabel("0 dB", alignment=Qt.AlignRight), num_rows // 2, 0)
        grid_layout.addWidget(QLabel("-18 dB", alignment=Qt.AlignRight), num_rows - 1, 0)

        # Crea 10 slider con etichette
        self.sliders = []
        for i, freq in enumerate(frequencies):
            # Etichetta per il valore sopra lo slider
            value_label = QLabel("0", alignment=Qt.AlignCenter)
            grid_layout.addWidget(value_label, 0, i + 1, 1, 1, alignment=Qt.AlignHCenter)

            # Slider verticale
            slider = QSlider(Qt.Vertical)
            slider.setMinimum(-18)
            slider.setMaximum(18)
            slider.setValue(0)
            slider.setTickPosition(QSlider.TicksBothSides)
            slider.setTickInterval(1)
            slider.valueChanged.connect(self.slider_value_changed)
            slider.value_label = value_label
            slider.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
            slider.setMinimumHeight(600)  # Imposta un'altezza minima per gli slider

            # Aggiungi lo slider alla griglia
            grid_layout.addWidget(slider, 1, i + 1, num_rows - 1, 1, alignment=Qt.AlignHCenter | Qt.AlignVCenter)

            # Etichetta per la frequenza sotto lo slider
            grid_layout.addWidget(QLabel(f"{freq}", alignment=Qt.AlignCenter), num_rows, i + 1, alignment=Qt.AlignHCenter)

            self.sliders.append(slider)

        # Imposta il layout griglia sul widget centrale
        central_widget.setLayout(grid_layout)

    def slider_value_changed(self, value):
        # Ottiene il riferimento allo slider che ha cambiato valore
        slider = self.sender()
        slider.value_label.setText(f"{value}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SliderWindow()
    window.show()
    sys.exit(app.exec_())
