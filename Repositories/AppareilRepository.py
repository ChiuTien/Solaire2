from Connection.Connexion import SQLServerDB
from Models.Appareil import Appareil


class AppareilRepository:
    def __init__(self):
        self.db = SQLServerDB()

    def create(self, appareil):
        """Insert a new appareil"""
        try:
            query = "INSERT INTO appareil (nom) VALUES (?)"
            params = (appareil.get_nom(),)
            self.db.execute(query, params)
            return True
        except Exception as e:
            print(f"Erreur lors de la création: {e}")
            return False

    def get_by_id(self, id_appareil):
        """Get an appareil by ID"""
        try:
            query = "SELECT * FROM appareil WHERE idAppareil = ?"
            result = self.db.fetch_all(query, (id_appareil,))
            if result:
                row = result[0]
                appareil = Appareil(row[0], row[1])
                return appareil
            return None
        except Exception as e:
            print(f"Erreur lors de la lecture: {e}")
            return None

    def get_all(self):
        """Get all appareils"""
        try:
            query = "SELECT * FROM appareil"
            result = self.db.fetch_all(query)
            appareils = []
            for row in result:
                appareil = Appareil(row[0], row[1])
                appareils.append(appareil)
            return appareils
        except Exception as e:
            print(f"Erreur lors de la lecture: {e}")
            return []

    def update(self, appareil):
        """Update an appareil"""
        try:
            query = "UPDATE appareil SET nom = ? WHERE idAppareil = ?"
            params = (appareil.get_nom(), appareil.get_idAppareil())
            self.db.execute(query, params)
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour: {e}")
            return False

    def delete(self, id_appareil):
        """Delete an appareil"""
        try:
            query = "DELETE FROM appareil WHERE idAppareil = ?"
            self.db.execute(query, (id_appareil,))
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            return False
