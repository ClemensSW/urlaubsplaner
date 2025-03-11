import json
import os
from pathlib import Path
import time

class DataStore:
    """
    Eine einfache Datenabstraktionsschicht, die JSON-Dateien anstelle einer Datenbank verwendet.
    Jede Entität (Benutzer, Teams, Urlaubsanträge) wird in einer separaten JSON-Datei gespeichert.
    """
    
    def __init__(self, data_dir="data"):
        # Stellen Sie sicher, dass das Datenverzeichnis existiert
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Pfade zu den Datendateien
        self.users_file = self.data_dir / "users.json"
        self.teams_file = self.data_dir / "teams.json"
        self.vacation_requests_file = self.data_dir / "vacation_requests.json"
        
        # Initialisieren Sie die Datendateien, falls sie nicht existieren
        self._initialize_files()
    
    def _initialize_files(self):
        """Initialisieren Sie die Datendateien, falls sie nicht existieren"""
        # Benutzer-Datei
        if not self.users_file.exists():
            self._save_data(self.users_file, [])
        
        # Teams-Datei
        if not self.teams_file.exists():
            self._save_data(self.teams_file, [])
        
        # Urlaubsanträge-Datei
        if not self.vacation_requests_file.exists():
            self._save_data(self.vacation_requests_file, [])
    
    def _load_data(self, file_path):
        """Laden Sie Daten aus einer JSON-Datei"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_data(self, file_path, data):
        """Speichern Sie Daten in einer JSON-Datei"""
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    
    def _generate_id(self):
        """Generieren Sie eine eindeutige ID basierend auf der aktuellen Zeit"""
        return str(int(time.time() * 1000))
    
    # Benutzer-Operationen
    def get_all_users(self):
        """Alle Benutzer abrufen"""
        return self._load_data(self.users_file)
    
    def get_user(self, user_id=None, email=None, phone=None):
        """
        Einen Benutzer nach ID, E-Mail oder Telefonnummer abrufen
        
        Args:
            user_id (str, optional): Benutzer-ID
            email (str, optional): E-Mail-Adresse
            phone (str, optional): Telefonnummer
            
        Returns:
            dict or None: Benutzerdaten oder None, wenn kein Benutzer gefunden wird
        """
        users = self.get_all_users()
        
        for user in users:
            if user_id and str(user.get('user_id', '')) == str(user_id):
                return user
            if email and user.get('email') == email:
                return user
            if phone and user.get('phone') == phone:
                return user
        
        return None
    
    def add_user(self, user_data):
        """
        Einen neuen Benutzer hinzufügen
        
        Args:
            user_data (dict): Benutzerdaten
            
        Returns:
            dict: Die hinzugefügten Benutzerdaten mit der ID
        """
        users = self.get_all_users()
        
        # Standardrolle hinzufügen, falls nicht angegeben
        if 'role' not in user_data:
            user_data['role'] = 'user'
        
        users.append(user_data)
        self._save_data(self.users_file, users)
        
        return user_data
    
    def update_user(self, user_id, updated_data):
        """
        Aktualisieren Sie einen vorhandenen Benutzer
        
        Args:
            user_id (str): Benutzer-ID
            updated_data (dict): Aktualisierte Benutzerdaten
            
        Returns:
            bool: True, wenn der Benutzer aktualisiert wurde, False sonst
        """
        users = self.get_all_users()
        
        for i, user in enumerate(users):
            if str(user.get('user_id', '')) == str(user_id):
                # Aktualisieren Sie die Benutzerdaten
                users[i].update(updated_data)
                self._save_data(self.users_file, users)
                return True
        
        return False
    
    def delete_user(self, user_id):
        """
        Löschen Sie einen Benutzer
        
        Args:
            user_id (str): Benutzer-ID
            
        Returns:
            bool: True, wenn der Benutzer gelöscht wurde, False sonst
        """
        users = self.get_all_users()
        
        for i, user in enumerate(users):
            if str(user.get('user_id', '')) == str(user_id):
                del users[i]
                self._save_data(self.users_file, users)
                return True
        
        return False
    
    # Teams-Operationen
    def get_all_teams(self):
        """Alle Teams abrufen"""
        return self._load_data(self.teams_file)
    
    def get_team(self, team_id):
        """Ein Team nach ID abrufen"""
        teams = self.get_all_teams()
        
        for team in teams:
            if str(team.get('id', '')) == str(team_id):
                return team
        
        return None
    
    def add_team(self, team_data):
        """Ein neues Team hinzufügen"""
        teams = self.get_all_teams()
        
        # ID hinzufügen, falls nicht angegeben
        if 'id' not in team_data:
            team_data['id'] = self._generate_id()
        
        teams.append(team_data)
        self._save_data(self.teams_file, teams)
        
        return team_data
    
    def update_team(self, team_id, updated_data):
        """Ein vorhandenes Team aktualisieren"""
        teams = self.get_all_teams()
        
        for i, team in enumerate(teams):
            if str(team.get('id', '')) == str(team_id):
                teams[i].update(updated_data)
                self._save_data(self.teams_file, teams)
                return True
        
        return False
    
    def delete_team(self, team_id):
        """Ein Team löschen"""
        teams = self.get_all_teams()
        
        for i, team in enumerate(teams):
            if str(team.get('id', '')) == str(team_id):
                del teams[i]
                self._save_data(self.teams_file, teams)
                return True
        
        return False
    
    # Urlaubsanträge-Operationen
    def get_all_vacation_requests(self):
        """Alle Urlaubsanträge abrufen"""
        return self._load_data(self.vacation_requests_file)
    
    def get_vacation_request(self, request_id):
        """Einen Urlaubsantrag nach ID abrufen"""
        requests = self.get_all_vacation_requests()
        
        for request in requests:
            if str(request.get('id', '')) == str(request_id):
                return request
        
        return None
    
    def add_vacation_request(self, request_data):
        """Einen neuen Urlaubsantrag hinzufügen"""
        requests = self.get_all_vacation_requests()
        
        # ID hinzufügen, falls nicht angegeben
        if 'id' not in request_data:
            request_data['id'] = self._generate_id()
        
        requests.append(request_data)
        self._save_data(self.vacation_requests_file, requests)
        
        return request_data
    
    def update_vacation_request(self, request_id, updated_data):
        """Einen vorhandenen Urlaubsantrag aktualisieren"""
        requests = self.get_all_vacation_requests()
        
        for i, request in enumerate(requests):
            if str(request.get('id', '')) == str(request_id):
                requests[i].update(updated_data)
                self._save_data(self.vacation_requests_file, requests)
                return True
        
        return False
    
    def delete_vacation_request(self, request_id):
        """Einen Urlaubsantrag löschen"""
        requests = self.get_all_vacation_requests()
        
        for i, request in enumerate(requests):
            if str(request.get('id', '')) == str(request_id):
                del requests[i]
                self._save_data(self.vacation_requests_file, requests)
                return True
        
        return False