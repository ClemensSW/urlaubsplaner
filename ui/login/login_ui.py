from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
from PyQt6.QtGui import QFont, QColor, QCursor, QPixmap

class RoundedButton(QPushButton):
    """Eine angepasste abgerundete Button-Klasse."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(50)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

class LoginUI(QMainWindow):
    """
    Die Benutzeroberfläche für das Login-Fenster.
    QMainWindow wird verwendet für bessere Kompatibilität mit Windows-Frames.
    """
    
    # Signale, die an den Controller gesendet werden
    closeClicked = pyqtSignal()
    loginClicked = pyqtSignal(str, str)  # username, password
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Fenstereinstellungen für modernes Aussehen
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Corporate Identity Farben
        self.primary_color = "#008D58"  # Dunkelgrün
        self.secondary_color = "#BCDBCB"  # Helles Grün
        self.dark_primary = "#006A42"  # Dunkleres Grün für Hover/Pressed
        
        # Drag-Unterstützung
        self.dragging = False
        self.drag_position = None
        
        # UI aufbauen
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        """Initialisiert die UI-Komponenten."""
        # Grundlegende Fenstereinstellungen
        self.setWindowTitle("Urlaubsübersicht - Anmeldung")
        self.setFixedSize(420, 600)  # Leicht erhöhte Höhe für bessere Kompatibilität
        
        # Zentrales Widget erstellen
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Haupt-Layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(0)
        
        # Hauptkarte mit Schatten
        self.card = QFrame()
        self.card.setObjectName("loginCard")
        
        # Schatten zur Karte hinzufügen
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.card.setGraphicsEffect(shadow)
        
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)
        
        # Header-Bereich mit Farbverlauf
        header = QFrame()
        header.setObjectName("loginHeader")
        header.setFixedHeight(180)
        header_layout = QVBoxLayout(header)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.setContentsMargins(30, 30, 30, 25)
        header_layout.setSpacing(15)
        
        # App-Logo
        logo_container = QFrame()
        logo_container.setFixedSize(80, 80)
        logo_container.setObjectName("logoContainer")
        
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        logo_icon = QLabel()
        logo_icon.setObjectName("logoIcon")
        logo_icon.setFixedSize(50, 50)
        logo_icon.setText("🗓️")
        logo_icon.setFont(QFont("Segoe UI", 28))
        logo_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_icon)
        
        header_layout.addWidget(logo_container, 0, Qt.AlignmentFlag.AlignCenter)
        
        # App-Titel
        title_label = QLabel("Urlaubsübersicht")
        title_label.setObjectName("appTitle")
        title_label.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title_label)
        
        card_layout.addWidget(header)
        
        # Inhaltsbereich
        content = QFrame()
        content.setObjectName("loginContent")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 30, 40, 40)
        content_layout.setSpacing(25)
        
        # Login-Titel
        login_label = QLabel("Anmeldung")
        login_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Medium))
        login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        login_label.setObjectName("loginLabel")
        content_layout.addWidget(login_label)
        
        # Benutzername-Feld
        username_layout = QVBoxLayout()
        username_layout.setSpacing(8)
        
        username_label = QLabel("Benutzername oder E-Mail")
        username_label.setObjectName("fieldLabel")
        username_label.setFont(QFont("Segoe UI", 11))
        
        self.username_input = QLineEdit()
        self.username_input.setObjectName("loginField")
        self.username_input.setPlaceholderText("Geben Sie Ihren Benutzernamen ein")
        self.username_input.setMinimumHeight(50)
        
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        content_layout.addLayout(username_layout)
        
        # Passwort-Feld
        password_layout = QVBoxLayout()
        password_layout.setSpacing(8)
        
        password_label = QLabel("Passwort")
        password_label.setObjectName("fieldLabel")
        password_label.setFont(QFont("Segoe UI", 11))
        
        self.password_input = QLineEdit()
        self.password_input.setObjectName("loginField")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Geben Sie Ihr Passwort ein")
        self.password_input.setMinimumHeight(50)
        
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        content_layout.addLayout(password_layout)
        
        # Login-Button
        self.login_button = RoundedButton("Anmelden")
        self.login_button.setObjectName("loginButton")
        self.login_button.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.login_button.setEnabled(False)  # Initial deaktiviert
        content_layout.addSpacing(10)
        content_layout.addWidget(self.login_button)
        
        # Info-Text
        info_label = QLabel("Im Prototyp können Sie sich mit 'admin' anmelden oder importierte Benutzer nutzen.")
        info_label.setObjectName("infoLabel")
        info_label.setWordWrap(True)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addSpacing(5)
        content_layout.addWidget(info_label)
        
        # Zum Layout hinzufügen
        card_layout.addWidget(content)
        main_layout.addWidget(self.card)
        
        # Schließen-Button
        self.close_button = QPushButton("×")
        self.close_button.setObjectName("closeButton")
        self.close_button.setFixedSize(30, 30)
        self.close_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.close_button.setParent(central_widget)
        self.close_button.move(380, 15)  # Positioniert am Ende des Headers
        
        # Signal-Verbindungen
        self.setup_connections()
        
        # Fokus auf Benutzername-Eingabe
        self.username_input.setFocus()
    
    def setup_connections(self):
        """Verbindet die UI-Ereignisse mit Signalen."""
        self.close_button.clicked.connect(self.closeClicked)
        self.login_button.clicked.connect(self.on_login_button_clicked)
        
        # Aktiviere/deaktiviere Login-Button basierend auf Eingabe
        self.username_input.textChanged.connect(self.update_login_button_state)
        self.password_input.textChanged.connect(self.update_login_button_state)
        
        # Enter-Taste zum Anmelden
        self.password_input.returnPressed.connect(self.on_login_button_clicked)
    
    def update_login_button_state(self):
        """Aktualisiert den Zustand des Login-Buttons basierend auf der Eingabe."""
        has_username = bool(self.username_input.text().strip())
        has_password = bool(self.password_input.text().strip())
        self.login_button.setEnabled(has_username and has_password)
    
    def on_login_button_clicked(self):
        """Sendet die Anmeldeinformationen an den Controller."""
        if self.login_button.isEnabled():
            username = self.username_input.text()
            password = self.password_input.text()
            self.loginClicked.emit(username, password)
    
    def apply_styles(self):
        """Wendet das moderne Styling mit Corporate Identity-Farben auf das Login-Fenster an."""
        self.setStyleSheet(f"""
            QWidget {{
                font-family: 'Segoe UI', 'Arial', sans-serif;
                color: #333333;
            }}
            
            QFrame#loginCard {{
                background-color: #ffffff;
                border-radius: 12px;
            }}
            
            QFrame#loginHeader {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                           stop:0 {self.primary_color}, stop:1 {self.dark_primary});
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
            }}
            
            QLabel#appTitle {{
                color: white;
                letter-spacing: 0.5px;
            }}
            
            QLabel#loginLabel {{
                color: #333333;
                letter-spacing: 0.4px;
            }}
            
            QFrame#logoContainer {{
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 40px;
            }}
            
            QLabel#logoIcon {{
                color: white;
            }}
            
            QFrame#loginContent {{
                background-color: white;
                border-bottom-left-radius: 12px;
                border-bottom-right-radius: 12px;
            }}
            
            QLabel#fieldLabel {{
                font-weight: 500;
                color: #555555;
                margin-left: 2px;
            }}
            
            QLineEdit#loginField {{
                background-color: #f5f5f5;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 6px 15px;
                color: #333333;
                font-size: 14px;
            }}
            
            QLineEdit#loginField:focus {{
                border: 2px solid {self.primary_color};
                background-color: #ffffff;
            }}
            
            QLineEdit#loginField:hover:!focus {{
                border: 2px solid {self.secondary_color};
            }}
            
            QPushButton#loginButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                           stop:0 {self.primary_color}, stop:1 {self.dark_primary});
                color: white;
                border: none;
                border-radius: 25px;
                padding: 12px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }}
            
            QPushButton#loginButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                           stop:0 #1a9d68, stop:1 #017a52);
            }}
            
            QPushButton#loginButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                           stop:0 {self.dark_primary}, stop:1 #005a38);
            }}
            
            QPushButton#loginButton:disabled {{
                background-color: #cccccc;
                color: #999999;
            }}
            
            QLabel#infoLabel {{
                color: #777777;
                font-style: italic;
                font-size: 12px;
            }}
            
            QPushButton#closeButton {{
                background-color: transparent;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border: none;
                border-radius: 15px;
            }}
            
            QPushButton#closeButton:hover {{
                background-color: rgba(255, 255, 255, 0.2);
            }}
            
            QPushButton#closeButton:pressed {{
                background-color: rgba(0, 0, 0, 0.1);
            }}
        """)
    
    def set_button_effect(self):
        """Setzt Effekte für den Login-Button."""
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(15)
        shadow_effect.setColor(QColor.fromString(self.primary_color))
        shadow_effect.setColor(QColor(0, 141, 88, 120))  # RGBA-Version von primary_color
        shadow_effect.setOffset(0, 4)
        self.login_button.setGraphicsEffect(shadow_effect)
    
    def set_success_effect(self):
        """Setzt einen visuellen Effekt für erfolgreiche Anmeldung."""
        success_effect = QGraphicsDropShadowEffect()
        success_effect.setBlurRadius(30)
        success_effect.setColor(QColor(0, 141, 88, 200))  # RGBA-Version von primary_color
        success_effect.setOffset(0, 0)
        self.card.setGraphicsEffect(success_effect)
    
    def mousePressEvent(self, event):
        """Verfolgt, wann das Ziehen beginnt."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Prüfe, ob der Mausklick in der obersten Hälfte des Headers ist - nur dort Ziehen erlauben
            if event.position().y() < 90:  # nur im oberen Bereich ziehen erlauben
                self.dragging = True
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                
                # Stelle sicher, dass dies nicht auf dem Schließen-Button ist
                if self.close_button and self.close_button.geometry().contains(event.position().toPoint()):
                    self.dragging = False
                    
                event.accept()
    
    def mouseReleaseEvent(self, event):
        """Verfolgt, wann das Ziehen endet."""
        self.dragging = False
        event.accept()
    
    def mouseMoveEvent(self, event):
        """Bewegt das Fenster beim Ziehen."""
        if self.dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()