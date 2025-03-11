from PyQt6.QtCore import pyqtSignal
from ui.login.login_ui import LoginUI
from ui.login.login_controller import LoginController

class LoginWindow(LoginUI):
    """
    Hauptklasse für das Login-Fenster, die UI und Controller verbindet.
    """
    
    # Signal bei erfolgreicher Anmeldung
    login_successful = pyqtSignal(str, str)  # username, role
    
    def __init__(self):
        super().__init__()
        
        # Controller erstellen und verbinden
        self.controller = LoginController(self)
        
        # Login erfolgreiche Signal verbinden
        self.controller.login_successful.connect(self.on_login_successful)
    
    def on_login_successful(self, username, role):
        """Wird aufgerufen, wenn die Anmeldung erfolgreich ist."""
        # Import hier erfolgt, um zirkuläre Importe zu vermeiden
        from ui.main_window import MainWindow
        
        # Login-Fenster schließen und Hauptfenster öffnen
        self.main_window = MainWindow(username, role, self.controller.data_store)
        self.main_window.show()
        self.close()