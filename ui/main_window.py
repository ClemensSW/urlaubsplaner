from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QStatusBar, QToolBar, QMessageBox, QFileDialog, 
                            QPushButton, QLineEdit, QGroupBox, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont
from utils.excel_handler import ExcelHandler

class MainWindow(QMainWindow):
    def __init__(self, username, role, data_store):
        super().__init__()
        self.username = username
        self.role = role
        self.data_store = data_store
        
        # Excel-Handler erstellen
        self.excel_handler = ExcelHandler(self.data_store)
        
        self.init_ui()
        
    def init_ui(self):
        # Fenstereigenschaften setzen
        self.setWindowTitle("Urlaubsantrags-Verwaltung")
        self.setMinimumSize(1024, 768)
        
        # Zentrales Widget und Hauptlayout erstellen
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Willkommenslabel erstellen
        welcome_label = QLabel(f"Willkommen, {self.username}! Rolle: {self.role}")
        welcome_label.setFont(QFont("Arial", 12))
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(welcome_label)
        
        # Tab-Widget für verschiedene Bereiche erstellen
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Tabs für verschiedene Module hinzufügen
        self.setup_dashboard_tab()
        self.setup_team_management_tab()
        self.setup_vacation_overview_tab()
        self.setup_import_tab()
        
        # Admin-Tabs nur für Admin-Benutzer anzeigen
        if self.role == "admin":
            self.setup_user_management_tab()
        
        # Statusleiste erstellen
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Bereit")
        
        # Menüleiste erstellen
        self.setup_menu_bar()
        
        # Werkzeugleiste erstellen
        self.setup_toolbar()
    
    def setup_dashboard_tab(self):
        # Dashboard-Tab erstellen - dies wird die Hauptübersicht sein
        dashboard_widget = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_widget)
        
        # Platzhalterinhalt
        dashboard_label = QLabel("Dashboard - Hier kommt eine Übersicht der wichtigsten Informationen")
        dashboard_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dashboard_layout.addWidget(dashboard_label)
        
        self.tab_widget.addTab(dashboard_widget, "Dashboard")
    
    def setup_team_management_tab(self):
        # Kolonnen-Verwaltungstab erstellen
        team_widget = QWidget()
        team_layout = QVBoxLayout(team_widget)
        
        # Platzhalterinhalt
        team_label = QLabel("Kolonnen-Verwaltung - Hier können Kolonnen erstellt und bearbeitet werden")
        team_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        team_layout.addWidget(team_label)
        
        self.tab_widget.addTab(team_widget, "Kolonnen-Verwaltung")
    
    def setup_vacation_overview_tab(self):
        # Urlaubsübersichtstab erstellen
        vacation_widget = QWidget()
        vacation_layout = QVBoxLayout(vacation_widget)
        
        # Platzhalterinhalt
        vacation_label = QLabel("Urlaubsübersicht - Hier wird die Jahresplanung angezeigt")
        vacation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vacation_layout.addWidget(vacation_label)
        
        self.tab_widget.addTab(vacation_widget, "Urlaubsübersicht")
    
    def setup_import_tab(self):
        # Import-Tab erstellen
        import_widget = QWidget()
        import_layout = QVBoxLayout(import_widget)
        import_layout.setSpacing(10)
        
        # Überschrift
        title_label = QLabel("Datenimport aus Excel-Dateien")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        import_layout.addWidget(title_label)
        
        # Trennlinie
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        import_layout.addWidget(line)
        import_layout.addSpacing(10)
        
        # Bereich für Nutzerimport
        user_import_group = QGroupBox("Nutzer importieren")
        user_import_layout = QVBoxLayout(user_import_group)
        
        # Beschreibung
        user_import_desc = QLabel(
            "Importieren Sie Nutzerdaten aus einer Excel-Datei. "
            "Die Datei sollte folgende Spalten enthalten:\n"
            "ID, Aktion, Sprache, Login-E-Mail, Login-Mobilnummer, Vorname, Nachname, "
            "Erstellungs-Datum, Öffentliche Telefonnummer, Abteilungsnummer, "
            "Position/Stellenbeschreibung, Geburtstag, Eintrittsdatum, "
            "Einladungs-Code, Onboarding-Status, App-Rolle"
        )
        user_import_desc.setWordWrap(True)
        user_import_layout.addWidget(user_import_desc)
        
        # Dateiauswahl und Import-Button
        file_layout = QHBoxLayout()
        self.user_file_path = QLineEdit()
        self.user_file_path.setReadOnly(True)
        self.user_file_path.setPlaceholderText("Wählen Sie eine Excel-Datei aus...")
        
        browse_button = QPushButton("Durchsuchen...")
        browse_button.clicked.connect(self.browse_user_file)
        
        import_button = QPushButton("Importieren")
        import_button.clicked.connect(self.import_users)
        
        file_layout.addWidget(self.user_file_path, 3)
        file_layout.addWidget(browse_button, 1)
        file_layout.addWidget(import_button, 1)
        
        user_import_layout.addLayout(file_layout)
        
        # Status-Label für Importergebnisse
        self.user_import_status = QLabel("")
        self.user_import_status.setWordWrap(True)
        user_import_layout.addWidget(self.user_import_status)
        
        import_layout.addWidget(user_import_group)
        
        # Bereich für Urlaubsanträge-Import
        vacation_import_group = QGroupBox("Urlaubsanträge importieren")
        vacation_import_layout = QVBoxLayout(vacation_import_group)
        
        # Beschreibung
        vacation_import_desc = QLabel(
            "Implementierung folgt in einem späteren Schritt."
        )
        vacation_import_desc.setWordWrap(True)
        vacation_import_layout.addWidget(vacation_import_desc)
        
        import_layout.addWidget(vacation_import_group)
        
        # Abstandshalter am Ende
        import_layout.addStretch()
        
        self.tab_widget.addTab(import_widget, "Daten importieren")
    
    def setup_user_management_tab(self):
        # Benutzerverwaltungstab erstellen (nur für Admins)
        user_widget = QWidget()
        user_layout = QVBoxLayout(user_widget)
        
        # Platzhalterinhalt
        user_label = QLabel("Benutzerverwaltung - Hier können Benutzer und Berechtigungen verwaltet werden")
        user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_layout.addWidget(user_label)
        
        self.tab_widget.addTab(user_widget, "Benutzerverwaltung")
    
    def setup_menu_bar(self):
        # Menüleiste erstellen
        menu_bar = self.menuBar()
        
        # Datei-Menü
        file_menu = menu_bar.addMenu("&Datei")
        
        # Aktionen zum Datei-Menü hinzufügen
        import_action = QAction("Excel importieren...", self)
        import_action.setStatusTip("Excel-Dateien aus der Mitarbeiter-App importieren")
        import_action.triggered.connect(self.show_import_tab)
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Beenden", self)
        exit_action.setStatusTip("Anwendung beenden")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Ansicht-Menü
        view_menu = menu_bar.addMenu("&Ansicht")
        
        dashboard_action = QAction("Dashboard", self)
        dashboard_action.setStatusTip("Dashboard anzeigen")
        dashboard_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(0))
        view_menu.addAction(dashboard_action)
        
        teams_action = QAction("Kolonnen-Verwaltung", self)
        teams_action.setStatusTip("Kolonnen verwalten")
        teams_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(1))
        view_menu.addAction(teams_action)
        
        vacation_action = QAction("Urlaubsübersicht", self)
        vacation_action.setStatusTip("Urlaubsübersicht anzeigen")
        vacation_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(2))
        view_menu.addAction(vacation_action)
        
        # Admin-Menü (nur für Admin-Benutzer angezeigt)
        if self.role == "admin":
            admin_menu = menu_bar.addMenu("&Administration")
            
            user_management_action = QAction("Benutzerverwaltung", self)
            user_management_action.setStatusTip("Benutzer verwalten")
            user_management_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(4))
            admin_menu.addAction(user_management_action)
        
        # Hilfe-Menü
        help_menu = menu_bar.addMenu("&Hilfe")
        
        about_action = QAction("Über", self)
        about_action.setStatusTip("Informationen über die Anwendung")
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
    
    def setup_toolbar(self):
        # Werkzeugleiste erstellen
        toolbar = QToolBar("Hauptwerkzeugleiste")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Aktionen zur Werkzeugleiste hinzufügen
        dashboard_action = QAction("Dashboard", self)
        dashboard_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(0))
        toolbar.addAction(dashboard_action)
        
        teams_action = QAction("Kolonnen", self)
        teams_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(1))
        toolbar.addAction(teams_action)
        
        vacation_action = QAction("Urlaub", self)
        vacation_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(2))
        toolbar.addAction(vacation_action)
        
        import_action = QAction("Import", self)
        import_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(3))
        toolbar.addAction(import_action)
    
    def show_import_tab(self):
        # Zum Import-Tab wechseln
        self.tab_widget.setCurrentIndex(3)
    
    def show_about_dialog(self):
        # Über-Dialog anzeigen
        QMessageBox.about(
            self,
            "Über Urlaubsantrags-Verwaltung",
            "Urlaubsantrags-Verwaltung\n"
            "Version 1.0\n\n"
            "Eine Anwendung zur Verwaltung von Urlaubsanträgen und Kolonnenplanung."
        )
    
    def browse_user_file(self):
        """Öffnet einen Dateiauswahldialog für Excel-Dateien"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Excel-Datei mit Nutzern auswählen",
            "",
            "Excel-Dateien (*.xlsx *.xls);;Alle Dateien (*)"
        )
        
        if file_path:
            self.user_file_path.setText(file_path)
            # Status zurücksetzen
            self.user_import_status.setText("")
    
    def import_users(self):
        """Importiert Nutzer aus der ausgewählten Excel-Datei"""
        file_path = self.user_file_path.text()
        
        if not file_path:
            self.user_import_status.setText("Bitte wählen Sie eine Datei aus.")
            return
        
        # Importieren und Ergebnis anzeigen
        success, message, count = self.excel_handler.import_users_from_excel(file_path)
        
        if success:
            self.user_import_status.setText(f"✅ {message}")
            self.status_bar.showMessage(f"{count} Benutzer erfolgreich importiert/aktualisiert", 5000)
        else:
            self.user_import_status.setText(f"❌ {message}")
            self.status_bar.showMessage("Fehler beim Importieren", 5000)
    
    def closeEvent(self, event):
        # Bestätigungsdialog vor dem Schließen anzeigen
        reply = QMessageBox.question(
            self,
            "Beenden bestätigen",
            "Möchten Sie die Anwendung wirklich beenden?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()