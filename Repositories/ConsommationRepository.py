from Connection.Connexion import SQLServerDB
from Models.Consommation import Consommation


class ConsommationRepository:
    def __init__(self):
        self.db = SQLServerDB()

    def create(self, consommation):
        """Insert a new consommation"""
        try:
            query = "INSERT INTO consommation (idAppareil, heureDebut, heureFin, consommation) VALUES (?, ?, ?, ?)"
            params = (
                consommation.get_idAppareil(),
                consommation.get_heureDebut(),
                consommation.get_heureFin(),
                consommation.get_consommation(),
            )
            self.db.execute(query, params)
            return True
        except Exception as e:
            print(f"Erreur lors de la création: {e}")
            return False

    def get_by_id(self, id_consommation):
        """Get a consommation by ID"""
        try:
            query = "SELECT * FROM consommation WHERE idConsommation = ?"
            result = self.db.fetch_all(query, (id_consommation,))
            if result:
                row = result[0]
                consommation = Consommation(row[0], row[1], row[2], row[3], row[4])
                return consommation
            return None
        except Exception as e:
            print(f"Erreur lors de la lecture: {e}")
            return None

    def get_all(self):
        """Get all consommations"""
        try:
            query = "SELECT * FROM consommation"
            result = self.db.fetch_all(query)
            consommations = []
            for row in result:
                consommation = Consommation(row[0], row[1], row[2], row[3], row[4])
                consommations.append(consommation)
            return consommations
        except Exception as e:
            print(f"Erreur lors de la lecture: {e}")
            return []

    def update(self, consommation):
        """Update a consommation"""
        try:
            query = "UPDATE consommation SET idAppareil = ?, heureDebut = ?, heureFin = ?, consommation = ? WHERE idConsommation = ?"
            params = (
                consommation.get_idAppareil(),
                consommation.get_heureDebut(),
                consommation.get_heureFin(),
                consommation.get_consommation(),
                consommation.get_idConsommation(),
            )
            self.db.execute(query, params)
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour: {e}")
            return False

    def delete(self, id_consommation):
        """Delete a consommation"""
        try:
            query = "DELETE FROM consommation WHERE idConsommation = ?"
            self.db.execute(query, (id_consommation,))
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            return False
