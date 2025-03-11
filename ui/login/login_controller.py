from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QColor
from data.data_store import DataStore
from utils.auth import Authentication

class LoginController(QObject):
    """
    Controller-Klasse für das Login-Fenster.
    Verarbeitet die Authentifizierung und Geschäftslogik.
    """
    
    # Signal wenn die Authentifizierung erfolgreich ist
    login_successful = pyqtSignal(str, str)  # username, role
    
    def __init__(self, ui, parent=None):
        super().__init__(parent)
        
        # Speichern der UI-Referenz
        self.ui = ui
        
        # Corporate Identity Farben
        self.primary_color = "#008D58"  # Dunkelgrün
        self.secondary_color = "#BCDBCB"  # Helles Grün
        
        # Daten und Authentifizierung einrichten
        self.data_store = DataStore()
        self.auth = Authentication(self.data_store)
        
        # UI-Signale verbinden
        self.connect_signals()
        
        # Administratorbenutzer sicherstellen
        self._ensure_admin_exists()
        
        # UI-Button-Effekte setzen
        self.ui.set_button_effect()
    
    def connect_signals(self):
        """Verbindet UI-Signale mit Controller-Methoden."""
        self.ui.closeClicked.connect(self.close)
        self.ui.loginClicked.connect(self.attempt_login)
    
    def _ensure_admin_exists(self):
        """Stellt sicher, dass ein Admin-Benutzer existiert."""
        admin_user = self.data_store.get_user(user_id="admin")
        
        if not admin_user:
            # Admin-Benutzer erstellen
            admin_data = {
                "user_id": "admin",
                "first_name": "Administrator",
                "last_name": "",
                "email": "admin@example.com",
                "role": "admin"
            }
            self.data_store.add_user(admin_data)
            print("Admin user created.")
    
    def attempt_login(self, username, password):
        """Versucht, den Benutzer anzumelden."""
        if not username:
            QMessageBox.warning(self.ui, "Fehler", "Bitte geben Sie Ihren Benutzernamen ein.")
            return
        
        # Authentifizierung
        success, user = self.auth.verify_credentials(username, password)
        
        if success:
            # Erfolgreiche Anmeldung - Effekt hinzufügen
            self.ui.set_success_effect()
            
            # Erfolgreiche Anmeldung
            role = user.get('role', 'user')
            first_name = user.get('first_name', username)
            self.login_successful.emit(first_name, role)
        else:
            # Benutzer nicht gefunden oder Passwort falsch
            error_message = QMessageBox(self.ui)
            error_message.setWindowTitle("Anmeldefehler")
            error_message.setIcon(QMessageBox.Icon.Warning)
            error_message.setText("Ungültiger Benutzername oder Passwort.")
            error_message.setInformativeText("Im Prototyp können Sie sich mit 'admin' anmelden.")
            error_message.setStandardButtons(QMessageBox.StandardButton.Ok)
            error_message.setStyleSheet(f"""
                QMessageBox {{
                    background-color: white;
                    color: #333333;
                }}
                QLabel {{
                    color: #333333;
                }}
                QPushButton {{
                    background-color: {self.primary_color};
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    background-color: #006A42;
                }}
            """)
            error_message.exec()
            
    def close(self):
        """Schließt das UI-Fenster."""
        self.ui.close()