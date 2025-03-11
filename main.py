import sys
import os
from PyQt6.QtWidgets import QApplication
from ui.login_window import LoginWindow

def main():
    # Anwendung initialisieren
    app = QApplication(sys.argv)
    app.setApplicationName("Urlaubsantrags-Verwaltung")
    
    # Sicherstellen, dass das data-Verzeichnis existiert
    os.makedirs("data", exist_ok=True)
    
    # Login-Fenster anzeigen
    login_window = LoginWindow()
    login_window.show()
    
    # Anwendung starten
    sys.exit(app.exec())

if __name__ == "__main__":
    main()