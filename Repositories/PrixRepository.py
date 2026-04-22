from Connection.Connexion import SQLServerDB
from Models.Prix import Prix


class PrixRepository:
    def __init__(self):
        self.db = SQLServerDB()

    def create(self, prix):
        """Insert a new prix"""
        try:
            query = "INSERT INTO prix (prixUnitaire, prixWeekend, EnergieSolaire) VALUES (?, ?, ?)"
            params = (
                prix.get_prixUnitaire(),
                prix.get_prixWeekend(),
                prix.get_EnergieSolaire(),
            )
            self.db.execute(query, params)
            return True
        except Exception as e:
            print(f"Erreur lors de la creation: {e}")
            return False

    def get_by_id(self, id_prix):
        """Get a prix by ID"""
        try:
            query = "SELECT * FROM prix WHERE id = ?"
            result = self.db.fetch_all(query, (id_prix,))
            if result:
                row = result[0]
                prix = Prix(row[0], row[1], row[2], row[3])
                return prix
            return None
        except Exception as e:
            print(f"Erreur lors de la lecture: {e}")
            return None

    def get_all(self):
        """Get all prix"""
        try:
            query = "SELECT * FROM prix"
            result = self.db.fetch_all(query)
            prix_list = []
            for row in result:
                prix = Prix(row[0], row[1], row[2], row[3])
                prix_list.append(prix)
            return prix_list
        except Exception as e:
            print(f"Erreur lors de la lecture: {e}")
            return []

    def update(self, prix):
        """Update a prix"""
        try:
            query = "UPDATE prix SET prixUnitaire = ?, prixWeekend = ?, EnergieSolaire = ? WHERE id = ?"
            params = (
                prix.get_prixUnitaire(),
                prix.get_prixWeekend(),
                prix.get_EnergieSolaire(),
                prix.get_id(),
            )
            self.db.execute(query, params)
            return True
        except Exception as e:
            print(f"Erreur lors de la mise a jour: {e}")
            return False

    def delete(self, id_prix):
        """Delete a prix"""
        try:
            query = "DELETE FROM prix WHERE id = ?"
            self.db.execute(query, (id_prix,))
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            return False
