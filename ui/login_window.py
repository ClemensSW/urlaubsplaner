from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from ui.main_window import MainWindow
from data.data_store import DataStore
from utils.auth import Authentication

class LoginWindow(QWidget):
    # Signal wenn Authentifizierung erfolgreich ist
    login_successful = pyqtSignal(str, str)  # username, role
    
    def __init__(self):
        super().__init__()
        
        # Datenspeicher erstellen
        self.data_store = DataStore()
        
        # Authentifizierungshelper erstellen
        self.auth = Authentication(self.data_store)
        
        self.init_ui()
        
    def init_ui(self):
        # Fenstereigenschaften setzen
        self.setWindowTitle("Anmeldung - Urlaubsantrags-Verwaltung")
        self.setFixedSize(400, 300)
        
        # Hauptlayout erstellen
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        
        # App-Titel hinzufügen
        title_label = QLabel("Urlaubsantrags-Verwaltung")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Eine Trennlinie hinzufügen
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)
        main_layout.addSpacing(20)
        
        # Benutzername-Feld
        username_layout = QHBoxLayout()
        username_label = QLabel("Benutzername:")
        username_label.setFixedWidth(100)
        self.username_input = QLineEdit()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        main_layout.addLayout(username_layout)
        
        # Passwort-Feld
        password_layout = QHBoxLayout()
        password_label = QLabel("Passwort:")
        password_label.setFixedWidth(100)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        main_layout.addLayout(password_layout)
        
        main_layout.addSpacing(20)
        
        # Anmelde-Button
        self.login_button = QPushButton("Anmelden")
        self.login_button.setFixedHeight(40)
        self.login_button.clicked.connect(self.attempt_login)
        main_layout.addWidget(self.login_button)
        
        # Abstand am Ende hinzufügen
        main_layout.addStretch()
        
        # Layout setzen
        self.setLayout(main_layout)
        
        # Signale verbinden
        self.login_successful.connect(self.on_login_successful)
        
        # Fokus auf Benutzernamen-Eingabe setzen
        self.username_input.setFocus()
        
        # Admin-Benutzer erstellen, falls noch keiner existiert
        self._ensure_admin_exists()
        
    def _ensure_admin_exists(self):
        """Stellt sicher, dass ein Admin-Benutzer existiert"""
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
            print("Admin-Benutzer erstellt.")
        
    def attempt_login(self):
        """Versucht, den Benutzer anzumelden"""
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Fehler", "Bitte geben Sie Benutzername und Passwort ein.")
            return
        
        # Authentifizierung
        success, user = self.auth.verify_credentials(username, password)
        
        if success:
            # Login erfolgreich
            role = user.get('role', 'user')
            first_name = user.get('first_name', username)
            self.login_successful.emit(first_name, role)
        else:
            # Benutzer nicht gefunden oder Passwort falsch
            QMessageBox.warning(
                self, 
                "Anmeldefehler", 
                "Ungültiger Benutzername oder Passwort.\n\nHinweis im Prototyp: Sie können sich mit 'admin' anmelden oder importieren Sie zuerst Benutzer."
            )
        
    def on_login_successful(self, username, role):
        """Wird aufgerufen, wenn die Anmeldung erfolgreich war"""
        # Login-Fenster schließen und Hauptfenster öffnen
        self.main_window = MainWindow(username, role, self.data_store)
        self.main_window.show()
        self.close()