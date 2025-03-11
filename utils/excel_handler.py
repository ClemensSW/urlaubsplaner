import pandas as pd
import datetime
import os

class ExcelHandler:
    def __init__(self, data_store):
        self.data_store = data_store
    
    def import_users_from_excel(self, file_path):
        """
        Importiert Benutzer aus einer Excel-Datei in den Datenspeicher
        
        Args:
            file_path (str): Pfad zur Excel-Datei
            
        Returns:
            tuple: (success, message, user_count)
        """
        try:
            # Überprüfen, ob die Datei existiert
            if not os.path.exists(file_path):
                return False, f"Datei nicht gefunden: {file_path}", 0
            
            # Excel-Datei laden
            df = pd.read_excel(file_path)
            
            # Überprüfen, ob die erforderlichen Spalten vorhanden sind
            required_columns = [
                "ID", "Vorname", "Nachname"
            ]
            
            for col in required_columns:
                if col not in df.columns:
                    return False, f"Erforderliche Spalte '{col}' nicht gefunden", 0
            
            # Zähler für importierte Benutzer
            imported_count = 0
            updated_count = 0
            
            # Benutzer in den Datenspeicher einfügen
            for _, row in df.iterrows():
                # Überprüfen, ob der Benutzer bereits existiert
                existing_user = self.data_store.get_user(user_id=row["ID"])
                
                # Daten für den Benutzer vorbereiten
                user_data = {
                    "user_id": str(row["ID"]),
                    "first_name": row["Vorname"],
                    "last_name": row["Nachname"],
                    "email": row["Login-E-Mail"] if "Login-E-Mail" in row and pd.notna(row["Login-E-Mail"]) else None,
                    "phone": row["Login-Mobilnummer"] if "Login-Mobilnummer" in row and pd.notna(row["Login-Mobilnummer"]) else None,
                    "department": str(row["Abteilungsnummer"]) if "Abteilungsnummer" in row and pd.notna(row["Abteilungsnummer"]) else None,
                    "position": row["Position/Stellenbeschreibung"] if "Position/Stellenbeschreibung" in row and pd.notna(row["Position/Stellenbeschreibung"]) else None,
                    "birthday": self._format_date(row.get("Geburtstag")) if "Geburtstag" in row and pd.notna(row.get("Geburtstag")) else None,
                    "entry_date": self._format_date(row.get("Eintrittsdatum")) if "Eintrittsdatum" in row and pd.notna(row.get("Eintrittsdatum")) else None,
                    "role": "user"  # Standardrolle
                }
                
                if existing_user:
                    # Vorhandenen Benutzer aktualisieren
                    self.data_store.update_user(user_data["user_id"], user_data)
                    updated_count += 1
                else:
                    # Neuen Benutzer hinzufügen
                    self.data_store.add_user(user_data)
                    imported_count += 1
            
            return True, f"{imported_count} Benutzer importiert, {updated_count} Benutzer aktualisiert", imported_count + updated_count
            
        except Exception as e:
            return False, f"Fehler beim Importieren: {str(e)}", 0
    
    def import_vacation_requests_from_excel(self, file_path):
        """
        Importiert Urlaubsanträge aus einer Excel-Datei in den Datenspeicher
        
        Args:
            file_path (str): Pfad zur Excel-Datei
            
        Returns:
            tuple: (success, message, request_count)
        """
        try:
            # Diese Funktion würde ähnlich wie import_users_from_excel implementiert werden
            # Für jetzt geben wir einen Platzhalter zurück
            return False, "Diese Funktion ist noch nicht implementiert", 0
            
        except Exception as e:
            return False, f"Fehler beim Importieren: {str(e)}", 0
    
    def _format_date(self, date_value):
        """Formatiert ein Datum für den Datenspeicher"""
        if isinstance(date_value, datetime.datetime) or isinstance(date_value, datetime.date):
            return date_value.strftime("%Y-%m-%d")
        elif isinstance(date_value, str):
            return date_value
        return None