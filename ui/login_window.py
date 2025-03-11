from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QMessageBox, QFrame, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QIcon, QPalette, QColor
from data.data_store import DataStore
from utils.auth import Authentication

class LoginWindow(QWidget):
    # Signal when authentication is successful
    login_successful = pyqtSignal(str, str)  # username, role
    
    def __init__(self):
        super().__init__()
        
        # Create data store
        self.data_store = DataStore()
        
        # Create authentication helper
        self.auth = Authentication(self.data_store)
        
        self.init_ui()
        self.apply_dark_theme()
        
    def init_ui(self):
        # Set window properties
        self.setWindowTitle("Urlaubsplaner Pro - Anmeldung")
        self.setFixedSize(450, 500)
        
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create header section
        header = QFrame()
        header.setObjectName("loginHeader")
        header.setFixedHeight(150)
        header_layout = QVBoxLayout(header)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # App logo (placeholder)
        logo_label = QLabel()
        logo_label.setFixedSize(80, 80)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setObjectName("logoLabel")
        header_layout.addWidget(logo_label)
        
        # App title
        title_label = QLabel("Urlaubsplaner Pro")
        title_label.setObjectName("appTitle")
        title_label.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title_label)
        
        main_layout.addWidget(header)
        
        # Create content section
        content = QFrame()
        content.setObjectName("loginContent")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(50, 40, 50, 40)
        content_layout.setSpacing(20)
        
        # Login form title
        login_label = QLabel("Anmeldung")
        login_label.setFont(QFont("Segoe UI", 16))
        login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(login_label)
        content_layout.addSpacing(20)
        
        # Username field
        username_layout = QVBoxLayout()
        username_label = QLabel("Benutzername oder E-Mail")
        username_label.setObjectName("fieldLabel")
        
        self.username_input = QLineEdit()
        self.username_input.setObjectName("loginField")
        self.username_input.setPlaceholderText("Geben Sie Ihren Benutzernamen ein")
        self.username_input.setMinimumHeight(40)
        
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        content_layout.addLayout(username_layout)
        
        # Password field
        password_layout = QVBoxLayout()
        password_label = QLabel("Passwort")
        password_label.setObjectName("fieldLabel")
        
        self.password_input = QLineEdit()
        self.password_input.setObjectName("loginField")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Geben Sie Ihr Passwort ein")
        self.password_input.setMinimumHeight(40)
        
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        content_layout.addLayout(password_layout)
        
        content_layout.addSpacing(20)
        
        # Login button
        self.login_button = QPushButton("Anmelden")
        self.login_button.setObjectName("loginButton")
        self.login_button.setMinimumHeight(45)
        self.login_button.clicked.connect(self.attempt_login)
        content_layout.addWidget(self.login_button)
        
        # Info text for prototype
        info_label = QLabel("Im Prototyp können Sie sich mit 'admin' anmelden oder importierte Benutzer nutzen.")
        info_label.setObjectName("infoLabel")
        info_label.setWordWrap(True)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(info_label)
        
        # Stretch to push everything to the top
        content_layout.addStretch()
        
        main_layout.addWidget(content)
        
        # Create footer section
        footer = QFrame()
        footer.setObjectName("loginFooter")
        footer.setFixedHeight(50)
        footer_layout = QHBoxLayout(footer)
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        version_label = QLabel("Version 1.0")
        version_label.setObjectName("versionLabel")
        footer_layout.addWidget(version_label)
        
        main_layout.addWidget(footer)
        
        # Connect signals
        self.login_successful.connect(self.on_login_successful)
        
        # Set focus to username input
        self.username_input.setFocus()
        
        # Create admin user if none exists
        self._ensure_admin_exists()
    
    def apply_dark_theme(self):
        """Apply dark theme to the login window"""
        # Define dark theme color palette
        palette = QPalette()
        
        # Base colors
        palette.setColor(QPalette.ColorRole.Window, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(212, 212, 212))
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.Text, QColor(212, 212, 212))
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(212, 212, 212))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
        
        # Apply the palette
        self.setPalette(palette)
        
        # Additional styling with stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                color: #d4d4d4;
            }
            
            QFrame#loginHeader {
                background-color: #1e5aa0;
                color: white;
            }
            
            QLabel#appTitle {
                color: white;
            }
            
            QLabel#logoLabel {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 40px;
            }
            
            QFrame#loginContent {
                background-color: #2d2d2d;
            }
            
            QLabel#fieldLabel {
                font-weight: bold;
                color: #a9a9a9;
            }
            
            QLineEdit#loginField {
                background-color: #383838;
                border: 1px solid #505050;
                border-radius: 3px;
                padding: 5px 10px;
                color: #d4d4d4;
            }
            
            QLineEdit#loginField:focus {
                border: 1px solid #1e5aa0;
            }
            
            QPushButton#loginButton {
                background-color: #1e5aa0;
                border: none;
                border-radius: 3px;
                color: white;
                font-weight: bold;
            }
            
            QPushButton#loginButton:hover {
                background-color: #2a6bc0;
            }
            
            QPushButton#loginButton:pressed {
                background-color: #0d4a90;
            }
            
            QLabel#infoLabel {
                color: #a0a0a0;
                font-style: italic;
            }
            
            QFrame#loginFooter {
                background-color: #232323;
                color: #a0a0a0;
            }
            
            QLabel#versionLabel {
                color: #a0a0a0;
            }
        """)
        
    def _ensure_admin_exists(self):
        """Make sure an admin user exists"""
        admin_user = self.data_store.get_user(user_id="admin")
        
        if not admin_user:
            # Create admin user
            admin_data = {
                "user_id": "admin",
                "first_name": "Administrator",
                "last_name": "",
                "email": "admin@example.com",
                "role": "admin"
            }
            self.data_store.add_user(admin_data)
            print("Admin user created.")
        
    def attempt_login(self):
        """Attempt to log in the user"""
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username:
            QMessageBox.warning(self, "Fehler", "Bitte geben Sie Ihren Benutzernamen ein.")
            return
        
        # Authentication
        success, user = self.auth.verify_credentials(username, password)
        
        if success:
            # Login successful
            role = user.get('role', 'user')
            first_name = user.get('first_name', username)
            self.login_successful.emit(first_name, role)
        else:
            # User not found or password incorrect
            QMessageBox.warning(
                self, 
                "Anmeldefehler", 
                "Ungültiger Benutzername oder Passwort.\n\nHinweis: Im Prototyp können Sie sich mit 'admin' anmelden."
            )
        
    def on_login_successful(self, username, role):
        """Called when login is successful"""
        # Import done here to avoid circular imports
        from ui.main_window import MainWindow
        
        # Close login window and open main window
        self.main_window = MainWindow(username, role, self.data_store)
        self.main_window.show()
        self.close()