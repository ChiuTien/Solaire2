from Connection.Connexion import SQLServerDB
from Models.HeurePointe import HeurePointe


class HeurePointeRepository:
    def __init__(self):
        self.db = SQLServerDB()

    def create(self, heure_pointe):
        """Insert a new heure_pointe"""
        try:
            query = "INSERT INTO Heure_pointe (heureDebut, heureFin, pourcentage) VALUES (?, ?, ?)"
            params = (
                heure_pointe.get_heureDebut(),
                heure_pointe.get_heureFin(),
                heure_pointe.get_pourcentage(),
            )
            self.db.execute(query, params)
            return True
        except Exception as e:
            print(f"Erreur lors de la creation: {e}")
            return False

    def get_by_id(self, id_heure_pointe):
        """Get an heure_pointe by ID"""
        try:
            query = "SELECT * FROM Heure_pointe WHERE id = ?"
            result = self.db.fetch_all(query, (id_heure_pointe,))
            if result:
                row = result[0]
                heure_pointe = HeurePointe(row[0], row[1], row[2], row[3])
                return heure_pointe
            return None
        except Exception as e:
            print(f"Erreur lors de la lecture: {e}")
            return None

    def get_all(self):
        """Get all heures de pointe"""
        try:
            query = "SELECT * FROM Heure_pointe"
            result = self.db.fetch_all(query)
            heure_pointes = []
            for row in result:
                heure_pointe = HeurePointe(row[0], row[1], row[2], row[3])
                heure_pointes.append(heure_pointe)
            return heure_pointes
        except Exception as e:
            print(f"Erreur lors de la lecture: {e}")
            return []

    def update(self, heure_pointe):
        """Update an heure_pointe"""
        try:
            query = "UPDATE Heure_pointe SET heureDebut = ?, heureFin = ?, pourcentage = ? WHERE id = ?"
            params = (
                heure_pointe.get_heureDebut(),
                heure_pointe.get_heureFin(),
                heure_pointe.get_pourcentage(),
                heure_pointe.get_id(),
            )
            self.db.execute(query, params)
            return True
        except Exception as e:
            print(f"Erreur lors de la mise a jour: {e}")
            return False

    def delete(self, id_heure_pointe):
        """Delete an heure_pointe"""
        try:
            query = "DELETE FROM Heure_pointe WHERE id = ?"
            self.db.execute(query, (id_heure_pointe,))
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            return False
