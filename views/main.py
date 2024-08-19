import sys
import os

# Aggiungi la directory principale del progetto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt5.QtWidgets import QApplication
from ui_manager import UIManager

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Applica il file di stile QSS
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = UIManager()
    window.show()
    sys.exit(app.exec_())