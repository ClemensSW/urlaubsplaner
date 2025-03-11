from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QGridLayout, QScrollArea, QFrame, QComboBox, 
                             QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
                             QHeaderView, QAbstractItemView, QSpacerItem)
from PyQt6.QtCore import Qt, QSize, QDate
from PyQt6.QtGui import QColor, QFont, QBrush
import calendar
from datetime import datetime, timedelta

class AnnualVacationOverview(QWidget):
    """
    A component showing the annual vacation overview for teams/employees
    similar to an Excel spreadsheet visualization
    """
    
    def __init__(self, data_store, parent=None):
        super().__init__(parent)
        self.data_store = data_store
        
        # Current view settings
        self.current_year = datetime.now().year
        self.selected_department = None
        
        # Used for managing color codes
        self.vacation_colors = {
            "approved": QColor(60, 179, 113),  # Green for approved vacation
            "pending": QColor(255, 165, 0),    # Orange for pending
            "rejected": QColor(220, 20, 60),   # Red for rejected
            "holiday": QColor(70, 130, 180),   # Steel blue for public holidays
            "weekend": QColor(95, 95, 95)      # Grey for weekends
        }
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create controls panel
        self.create_controls()
        main_layout.addWidget(self.controls_frame)
        
        # Create legend for color codes
        self.create_legend()
        main_layout.addWidget(self.legend_frame)
        
        # Create the annual calendar grid
        self.create_calendar_grid()
        
        # Add the calendar area to the main layout
        main_layout.addWidget(self.scroll_area, 1)  # Give it stretch factor to fill space
        
    def create_controls(self):
        """Create the controls panel with filters and actions"""
        self.controls_frame = QFrame()
        self.controls_frame.setObjectName("controlsFrame")
        self.controls_frame.setMinimumHeight(60)
        self.controls_frame.setMaximumHeight(60)
        
        controls_layout = QHBoxLayout(self.controls_frame)
        controls_layout.setContentsMargins(20, 10, 20, 10)
        
        # Year selector
        year_label = QLabel("Jahr:")
        self.year_combo = QComboBox()
        current_year = datetime.now().year
        for year in range(current_year - 2, current_year + 3):
            self.year_combo.addItem(str(year))
        self.year_combo.setCurrentText(str(current_year))
        self.year_combo.currentTextChanged.connect(self.on_year_changed)
        
        # Department filter (if applicable)
        dept_label = QLabel("Abteilung:")
        self.dept_combo = QComboBox()
        self.dept_combo.addItem("Alle Abteilungen")
        # Add departments from data store in a real implementation
        self.dept_combo.addItem("IT")
        self.dept_combo.addItem("Produktion")
        self.dept_combo.addItem("Vertrieb")
        self.dept_combo.currentTextChanged.connect(self.on_department_changed)
        
        # View options
        view_label = QLabel("Anzeige:")
        self.view_combo = QComboBox()
        self.view_combo.addItem("Kolonne")
        self.view_combo.addItem("Mitarbeiter")
        self.view_combo.currentTextChanged.connect(self.on_view_changed)
        
        # Export button
        self.export_btn = QPushButton("Excel exportieren")
        self.export_btn.clicked.connect(self.on_export)
        
        # Add widgets to layout
        controls_layout.addWidget(year_label)
        controls_layout.addWidget(self.year_combo)
        controls_layout.addSpacing(20)
        controls_layout.addWidget(dept_label)
        controls_layout.addWidget(self.dept_combo)
        controls_layout.addSpacing(20)
        controls_layout.addWidget(view_label)
        controls_layout.addWidget(self.view_combo)
        controls_layout.addStretch()
        controls_layout.addWidget(self.export_btn)
    
    def create_legend(self):
        """Create the legend explaining color codes"""
        self.legend_frame = QFrame()
        self.legend_frame.setObjectName("legendFrame")
        self.legend_frame.setMinimumHeight(40)
        self.legend_frame.setMaximumHeight(40)
        
        legend_layout = QHBoxLayout(self.legend_frame)
        legend_layout.setContentsMargins(20, 5, 20, 5)
        
        # Create legend items
        legend_items = [
            ("Genehmigter Urlaub", self.vacation_colors["approved"]),
            ("Ausstehender Urlaub", self.vacation_colors["pending"]),
            ("Feiertag", self.vacation_colors["holiday"]),
            ("Wochenende", self.vacation_colors["weekend"])
        ]
        
        for text, color in legend_items:
            # Create a colored box
            color_box = QFrame()
            color_box.setFixedSize(16, 16)
            color_box.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #555;")
            
            # Create label
            label = QLabel(text)
            
            # Create container for this legend item
            item_layout = QHBoxLayout()
            item_layout.setSpacing(5)
            item_layout.addWidget(color_box)
            item_layout.addWidget(label)
            
            # Add to legend
            legend_layout.addLayout(item_layout)
        
        # Add spacer at the end
        legend_layout.addStretch()
    
    def create_calendar_grid(self):
        """Create the annual calendar grid"""
        # Create a scroll area to contain the calendar
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create container widget
        calendar_container = QWidget()
        self.calendar_layout = QVBoxLayout(calendar_container)
        self.calendar_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create the calendar table
        self.calendar_table = QTableWidget()
        self.calendar_table.setObjectName("annualCalendar")
        self.calendar_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.calendar_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.calendar_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.calendar_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.calendar_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.calendar_table.setShowGrid(True)
        
        # Set cell size
        self.calendar_table.horizontalHeader().setDefaultSectionSize(18)
        self.calendar_table.verticalHeader().setDefaultSectionSize(30)
        
        # Add to layout
        self.calendar_layout.addWidget(self.calendar_table)
        self.scroll_area.setWidget(calendar_container)
        
        # Initialize with current year's data
        self.populate_annual_calendar()
        
    def populate_annual_calendar(self):
        """Populate the annual calendar with days and vacation data"""
        year = self.current_year
        
        # Calculate days in the year
        days_in_year = 366 if calendar.isleap(year) else 365
        
        # Set columns (days of the year)
        self.calendar_table.setColumnCount(days_in_year + 1)  # +1 for the name column
        
        # Create a date reference list for the entire year
        start_date = datetime(year, 1, 1)
        dates = [start_date + timedelta(days=i) for i in range(days_in_year)]
        
        # Create column headers (month abbreviations)
        month_headers = [""] + [date.strftime("%b") for date in dates]
        self.calendar_table.setHorizontalHeaderLabels(month_headers)
        
        # Format the month headers to show only at the start of each month
        for col in range(1, days_in_year + 1):
            date = dates[col-1]
            if date.day != 1:
                header_item = QTableWidgetItem("")
                self.calendar_table.setHorizontalHeaderItem(col, header_item)
        
        # Create row headers (team/employee names) using sample data
        teams = self.get_teams()
        row_count = len(teams)
        self.calendar_table.setRowCount(row_count)
        
        for row, team in enumerate(teams):
            self.calendar_table.setVerticalHeaderItem(row, QTableWidgetItem(team["name"]))
            
            # Create name column
            name_item = QTableWidgetItem(team["name"])
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            name_item.setBackground(QBrush(QColor(50, 50, 60)))
            name_item.setForeground(QBrush(QColor(220, 220, 220)))
            self.calendar_table.setItem(row, 0, name_item)
            
            # Fill in calendar cells for this team
            for col in range(1, days_in_year + 1):
                date = dates[col-1]
                
                # Create cell
                cell = QTableWidgetItem("")
                
                # Format weekends
                if date.weekday() >= 5:  # Saturday or Sunday
                    cell.setBackground(QBrush(self.vacation_colors["weekend"]))
                
                # Add some dummy vacation data for demonstration
                # In a real app, you'd get this from your data store
                import random
                if random.random() < 0.05:  # 5% chance of vacation
                    cell.setBackground(QBrush(self.vacation_colors["approved"]))
                    # For vacations that span multiple days, you would set the same background
                    # for the entire range
                
                self.calendar_table.setItem(row, col, cell)
        
        # Set first column width
        self.calendar_table.setColumnWidth(0, 180)
        
        # Find and highlight today
        today = datetime.now()
        if today.year == year:
            today_column = (today - start_date).days + 1
            for row in range(row_count):
                cell = self.calendar_table.item(row, today_column)
                if cell:
                    current_bg = cell.background().color()
                    # Only change background if it's not already a vacation
                    if current_bg == QColor(0, 0, 0, 0) or current_bg == self.vacation_colors["weekend"]:
                        border_style = "border: 2px solid #5f87ff;"
                        self.calendar_table.item(row, today_column).setData(
                            Qt.ItemDataRole.UserRole, 
                            "today"
                        )
    
    def get_teams(self):
        """Get teams data - would normally come from data_store"""
        # This is dummy data - in a real app, get from your data store
        return [
            {"id": "team1", "name": "Team 1", "members": 5},
            {"id": "team2", "name": "Team 2", "members": 4},
            {"id": "team3", "name": "Team 3", "members": 6},
            {"id": "team4", "name": "Team 4", "members": 3},
            {"id": "team5", "name": "Team 5", "members": 5},
            {"id": "team6", "name": "Team 6", "members": 7},
            {"id": "team7", "name": "Team 7", "members": 4},
            {"id": "team8", "name": "Team 8", "members": 5},
        ]
    
    # Event handlers
    def on_year_changed(self, year):
        """Handle year selection changed"""
        self.current_year = int(year)
        self.populate_annual_calendar()
    
    def on_department_changed(self, dept_name):
        """Handle department selection changed"""
        if dept_name == "Alle Abteilungen":
            self.selected_department = None
        else:
            self.selected_department = dept_name
        # Would filter teams based on department
        self.populate_annual_calendar()
    
    def on_view_changed(self, view_type):
        """Handle view type changed between team and employee view"""
        # Would update the view to show teams or individual employees
        self.populate_annual_calendar()
    
    def on_export(self):
        """Export the current view to Excel"""
        # Would implement Excel export functionality
        print("Exporting to Excel...")
        # In a real implementation, would use your Excel export functionality