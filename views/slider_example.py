import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QLabel, QVBoxLayout, QWidget # pylint: disable=no-name-in-module
from PyQt5.QtCore import Qt # pylint: disable=no-name-in-module

class SliderWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Slider Banda ")
        self.setGeometry(100, 100, 300, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.print_value_changed)

        self.label = QLabel("Value: 50")
        self.label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.slider)
        layout.addWidget(self.label)

        central_widget.setLayout(layout)

    def slider_value_changed(self, value):
        self.label.setText(f"Value: {value}")

    def print_value_changed(self, value):
        print(f"Value: {value}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SliderWindow()
    window.show()
    sys.exit(app.exec_())
