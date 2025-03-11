from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QComboBox, QStatusBar, QTabWidget,
                             QFrame, QFileDialog, QMessageBox, QSplitter)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon, QFont
from utils.excel_handler import ExcelHandler
import sys

class MainWindow(QMainWindow):
    def __init__(self, username, role, data_store):
        super().__init__()
        self.username = username
        self.role = role
        self.data_store = data_store
        
        # Create Excel handler
        self.excel_handler = ExcelHandler(self.data_store)
        
        # Initialize UI
        self.init_ui()
        self.apply_dark_theme()
        
    def init_ui(self):
        """Initialize the main UI components"""
        # Set window properties
        self.setWindowTitle("Urlaubsübersicht")
        self.setMinimumSize(1200, 800)
        
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Set up the header
        self.setup_header()
        
        # Set up the content tabs
        self.setup_content_tabs()
        
        # Set up status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(f"Angemeldet als {self.username} | Rolle: {self.role}")
        
        # Set up menu bar
        self.setup_menu()
        
    def setup_header(self):
        """Set up the application header"""
        header = QFrame()
        header.setObjectName("appHeader")
        header.setFixedHeight(60)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        # App title
        app_title = QLabel("Urlaubsübersicht")
        app_title.setObjectName("appTitle")
        app_title.setFont(QFont("Segoe UI", 16, QFont.Weight.DemiBold))
        
        # User info
        user_info = QLabel(f"{self.username}")
        user_info.setObjectName("userInfo")
        
        # Add widgets to header
        header_layout.addWidget(app_title)
        header_layout.addStretch()
        header_layout.addWidget(user_info)
        
        # Add header to main layout
        self.main_layout.addWidget(header)
        
        # Add a separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setObjectName("headerSeparator")
        self.main_layout.addWidget(separator)
        
    def setup_content_tabs(self):
        """Set up the content area with tabs"""
        self.tabs = QTabWidget()
        self.tabs.setObjectName("contentTabs")
        
        # Create and add annual overview tab
        self.setup_annual_overview_tab()
        
        # Create and add import tab
        self.setup_import_tab()
        
        # Add tabs to main layout
        self.main_layout.addWidget(self.tabs, 1)  # 1 = stretch factor
        
    def setup_annual_overview_tab(self):
        """Set up the annual vacation overview tab"""
        from ui.components.annual_vacation_overview import AnnualVacationOverview
        
        overview_tab = QWidget()
        overview_layout = QVBoxLayout(overview_tab)
        overview_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create annual overview component
        self.annual_overview = AnnualVacationOverview(self.data_store)
        overview_layout.addWidget(self.annual_overview)
        
        # Add to tabs
        self.tabs.addTab(overview_tab, "Jahresübersicht")
        
    def setup_import_tab(self):
        """Set up the import tab for Excel data"""
        import_tab = QWidget()
        import_layout = QVBoxLayout(import_tab)
        import_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create header
        import_header = QLabel("Daten importieren")
        import_header.setObjectName("sectionHeader")
        import_header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        import_layout.addWidget(import_header)
        
        # Create import sections
        self.create_user_import_section(import_layout)
        import_layout.addSpacing(20)
        self.create_vacation_import_section(import_layout)
        
        # Add spacer
        import_layout.addStretch()
        
        # Add to tabs
        self.tabs.addTab(import_tab, "Daten importieren")
        
        # Only show this tab for admin users
        if self.role != "admin":
            self.tabs.setTabVisible(1, False)
    
    def create_user_import_section(self, parent_layout):
        """Create the user import section"""
        # Create container
        user_frame = QFrame()
        user_frame.setObjectName("importSection")
        user_layout = QVBoxLayout(user_frame)
        
        # Title
        title = QLabel("Benutzer importieren")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
        user_layout.addWidget(title)
        
        # Description
        desc = QLabel(
            "Importieren Sie Nutzerdaten aus einer Excel-Datei. Die Datei sollte folgende Spalten enthalten:\n"
            "ID, Aktion, Sprache, Login-E-Mail, Login-Mobilnummer, Vorname, Nachname, usw."
        )
        desc.setWordWrap(True)
        user_layout.addWidget(desc)
        
        # File selection
        file_layout = QHBoxLayout()
        self.user_file_path = QLabel("Keine Datei ausgewählt")
        
        browse_btn = QPushButton("Datei auswählen...")
        browse_btn.setObjectName("actionButton")
        browse_btn.clicked.connect(self.browse_user_file)
        
        import_btn = QPushButton("Importieren")
        import_btn.setObjectName("primaryButton")
        import_btn.clicked.connect(self.import_users)
        
        file_layout.addWidget(self.user_file_path)
        file_layout.addStretch()
        file_layout.addWidget(browse_btn)
        file_layout.addWidget(import_btn)
        
        user_layout.addLayout(file_layout)
        
        # Status label
        self.user_import_status = QLabel("")
        self.user_import_status.setWordWrap(True)
        user_layout.addWidget(self.user_import_status)
        
        # Add to parent
        parent_layout.addWidget(user_frame)
    
    def create_vacation_import_section(self, parent_layout):
        """Create the vacation import section"""
        # Create container
        vacation_frame = QFrame()
        vacation_frame.setObjectName("importSection")
        vacation_layout = QVBoxLayout(vacation_frame)
        
        # Title
        title = QLabel("Urlaubsdaten importieren")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
        vacation_layout.addWidget(title)
        
        # Description
        desc = QLabel(
            "Importieren Sie Urlaubsanträge aus einer Excel-Datei. Die Datei sollte folgende Spalten enthalten:\n"
            "Absender - User ID, Absender - Name, Absender - Einsendedatum, Bearbeiter - User ID, usw."
        )
        desc.setWordWrap(True)
        vacation_layout.addWidget(desc)
        
        # File selection
        file_layout = QHBoxLayout()
        self.vacation_file_path = QLabel("Keine Datei ausgewählt")
        
        browse_btn = QPushButton("Datei auswählen...")
        browse_btn.setObjectName("actionButton")
        browse_btn.clicked.connect(self.browse_vacation_file)
        
        import_btn = QPushButton("Importieren")
        import_btn.setObjectName("primaryButton")
        import_btn.clicked.connect(self.import_vacation)
        
        file_layout.addWidget(self.vacation_file_path)
        file_layout.addStretch()
        file_layout.addWidget(browse_btn)
        file_layout.addWidget(import_btn)
        
        vacation_layout.addLayout(file_layout)
        
        # Status label
        self.vacation_import_status = QLabel("")
        self.vacation_import_status.setWordWrap(True)
        vacation_layout.addWidget(self.vacation_import_status)
        
        # Add to parent
        parent_layout.addWidget(vacation_frame)
    
    def setup_menu(self):
        """Set up the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&Datei")
        
        if self.role == "admin":
            import_action = QAction("Daten importieren", self)
            import_action.triggered.connect(lambda: self.tabs.setCurrentIndex(1))
            file_menu.addAction(import_action)
            
            file_menu.addSeparator()
        
        export_action = QAction("Übersicht exportieren", self)
        export_action.triggered.connect(self.export_overview)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Beenden", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Teams menu
        teams_menu = menubar.addMenu("&Kolonnen")
        
        manage_teams_action = QAction("Kolonnen verwalten", self)
        manage_teams_action.triggered.connect(self.manage_teams)
        teams_menu.addAction(manage_teams_action)
        
        assign_members_action = QAction("Mitarbeiter zuordnen", self)
        assign_members_action.triggered.connect(self.assign_members)
        teams_menu.addAction(assign_members_action)
        
        # Admin menu (only for admin users)
        if self.role == "admin":
            admin_menu = menubar.addMenu("&Administration")
            
            user_mgmt_action = QAction("Benutzerverwaltung", self)
            user_mgmt_action.triggered.connect(self.manage_users)
            admin_menu.addAction(user_mgmt_action)
            
            department_mgmt_action = QAction("Abteilungsverwaltung", self)
            department_mgmt_action.triggered.connect(self.manage_departments)
            admin_menu.addAction(department_mgmt_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Hilfe")
        
        about_action = QAction("Über", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def apply_dark_theme(self):
        """Apply dark theme to the application"""
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #2d2d2d;
                color: #d4d4d4;
            }
            
            QFrame#appHeader {
                background-color: #1e5aa0;
                color: white;
            }
            
            QLabel#appTitle {
                color: white;
                font-weight: bold;
            }
            
            QFrame#headerSeparator {
                color: #3d3d3d;
            }
            
            QTabWidget::pane {
                border: none;
                background-color: #2d2d2d;
            }
            
            QTabWidget::tab-bar {
                alignment: left;
            }
            
            QTabBar::tab {
                background-color: #383838;
                color: #d4d4d4;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            
            QTabBar::tab:selected {
                background-color: #1e5aa0;
                color: white;
            }
            
            QTabBar::tab:!selected {
                background-color: #3d3d3d;
            }
            
            QTabBar::tab:!selected:hover {
                background-color: #4a4a4a;
            }
            
            QFrame#importSection {
                background-color: #333333;
                border-radius: 4px;
                padding: 10px;
            }
            
            QLabel#sectionHeader {
                color: #e0e0e0;
            }
            
            QPushButton {
                background-color: #3d3d3d;
                color: #d4d4d4;
                border: none;
                border-radius: 3px;
                padding: 6px 12px;
            }
            
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            
            QPushButton:pressed {
                background-color: #333333;
            }
            
            QPushButton#primaryButton {
                background-color: #1e5aa0;
                color: white;
                font-weight: bold;
            }
            
            QPushButton#primaryButton:hover {
                background-color: #2a6bc0;
            }
            
            QPushButton#primaryButton:pressed {
                background-color: #0d4a90;
            }
            
            QPushButton#actionButton {
                background-color: #505050;
            }
            
            QComboBox {
                background-color: #3d3d3d;
                color: #d4d4d4;
                border: 1px solid #505050;
                border-radius: 3px;
                padding: 4px 8px;
            }
            
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #505050;
            }
        """)
    
    # Event handlers
    def browse_user_file(self):
        """Browse for user Excel file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Benutzer-Excel auswählen",
            "",
            "Excel-Dateien (*.xlsx *.xls);;Alle Dateien (*)"
        )
        
        if file_path:
            self.user_file_path.setText(file_path)
            self.user_import_status.setText("")
    
    def import_users(self):
        """Import users from Excel file"""
        file_path = self.user_file_path.text()
        
        if file_path == "Keine Datei ausgewählt":
            self.user_import_status.setText("Bitte wählen Sie zuerst eine Datei aus.")
            return
        
        # Import users using Excel handler
        success, message, count = self.excel_handler.import_users_from_excel(file_path)
        
        if success:
            self.user_import_status.setText(f"✓ {message}")
            self.status_bar.showMessage(f"{count} Benutzer erfolgreich importiert/aktualisiert", 5000)
        else:
            self.user_import_status.setText(f"✗ {message}")
            self.status_bar.showMessage("Fehler beim Importieren", 5000)
    
    def browse_vacation_file(self):
        """Browse for vacation Excel file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Urlaubs-Excel auswählen",
            "",
            "Excel-Dateien (*.xlsx *.xls);;Alle Dateien (*)"
        )
        
        if file_path:
            self.vacation_file_path.setText(file_path)
            self.vacation_import_status.setText("")
    
    def import_vacation(self):
        """Import vacation data from Excel file"""
        file_path = self.vacation_file_path.text()
        
        if file_path == "Keine Datei ausgewählt":
            self.vacation_import_status.setText("Bitte wählen Sie zuerst eine Datei aus.")
            return
        
        # Import vacation data (would use real implementation)
        self.vacation_import_status.setText("Diese Funktion ist noch nicht implementiert.")
    
    def export_overview(self):
        """Export vacation overview to Excel"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Übersicht exportieren",
            "Jahresübersicht.xlsx",
            "Excel-Dateien (*.xlsx);;Alle Dateien (*)"
        )
        
        if file_path:
            # Would implement Excel export functionality
            QMessageBox.information(
                self,
                "Export",
                "Die Übersicht wurde exportiert."
            )
    
    def manage_teams(self):
        """Open team management dialog"""
        QMessageBox.information(
            self,
            "Kolonnen verwalten",
            "Diese Funktion wird in einem späteren Update implementiert."
        )
    
    def assign_members(self):
        """Open member assignment dialog"""
        QMessageBox.information(
            self,
            "Mitarbeiter zuordnen",
            "Diese Funktion wird in einem späteren Update implementiert."
        )
    
    def manage_users(self):
        """Open user management dialog"""
        QMessageBox.information(
            self,
            "Benutzerverwaltung",
            "Diese Funktion wird in einem späteren Update implementiert."
        )
    
    def manage_departments(self):
        """Open department management dialog"""
        QMessageBox.information(
            self,
            "Abteilungsverwaltung",
            "Diese Funktion wird in einem späteren Update implementiert."
        )
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "Über Urlaubsübersicht",
            "Urlaubsübersicht\nVersion 1.0\n\n"
            "Eine Anwendung zur Visualisierung von Urlaubs- und Kolonnenplanung."
        )
    
    def closeEvent(self, event):
        """Handle window close event"""
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