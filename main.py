import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from ui.login_window import LoginWindow

def main():
    # Initialize application
    app = QApplication(sys.argv)
    app.setApplicationName("Urlaubsplaner Pro")
    
    # Set default font
    app.setFont(QFont("Segoe UI", 10))
    
    # Set application style
    app.setStyle("Fusion")  # Use Fusion style as base for custom dark theme
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Show login window
    login_window = LoginWindow()
    login_window.show()
    
    # Start application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()