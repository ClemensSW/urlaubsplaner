import hashlib
import secrets

class Authentication:
    def __init__(self, data_store):
        self.data_store = data_store
    
    def verify_credentials(self, username, password):
        """
        Verifiziert die Anmeldedaten eines Benutzers
        
        Args:
            username (str): Benutzername (E-Mail, Telefonnummer oder Benutzer-ID)
            password (str): Passwort
            
        Returns:
            tuple: (success, user_data)
        """
        # Für den Prototyp: Admin-Benutzer immer akzeptieren
        if username.lower() == "admin":
            admin_user = {
                "user_id": "admin",
                "first_name": "Administrator",
                "last_name": "",
                "email": "admin@example.com",
                "role": "admin"
            }
            return True, admin_user
        
        # Benutzer in den Daten suchen
        user = self.data_store.get_user(email=username)
        if not user:
            user = self.data_store.get_user(phone=username)
        if not user:
            user = self.data_store.get_user(user_id=username)
        
        if not user:
            return False, None
        
        # Für den Prototyp: Jedes Passwort akzeptieren
        # In einer echten Anwendung würden Sie Passwort-Hashing verwenden
        return True, user
    
    def hash_password(self, password):
        """
        Hasht ein Passwort zum sicheren Speichern
        
        Args:
            password (str): Das zu hashende Passwort
            
        Returns:
            str: Der Passwort-Hash im Format "salt$hash"
        """
        salt = secrets.token_hex(16)
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}${hashed}"
    
    def verify_password(self, stored_password, provided_password):
        """
        Überprüft ein Passwort gegen einen gespeicherten Hash
        
        Args:
            stored_password (str): Der gespeicherte Passwort-Hash
            provided_password (str): Das zu überprüfende Passwort
            
        Returns:
            bool: True, wenn das Passwort übereinstimmt, sonst False
        """
        # Wenn kein gespeichertes Passwort vorhanden ist, im Prototyp akzeptieren
        if not stored_password:
            return True
            
        salt, hashed = stored_password.split('$')
        calculated_hash = hashlib.sha256((provided_password + salt).encode()).hexdigest()
        return calculated_hash == hashed