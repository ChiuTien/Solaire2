from Connection.Connexion import SQLServerDB
from Models.Panneau import Panneau


class PanneauRepository:
    def __init__(self):
        self.db = SQLServerDB()

    def create(self, panneau):
        """Insert a new panneau"""
        try:
            query = "INSERT INTO panneau (nom, rendement, puissanceA, puissanceB, energie, prixUnitaire, prixWeekend) VALUES (?, ?, ?, ?, ?, ?, ?)"
            params = (
                panneau.get_nom(),
                panneau.get_rendement(),
                panneau.get_puissanceA(),
                panneau.get_puissanceB(),
                panneau.get_energie(),
                panneau.get_prixUnitaire(),
                panneau.get_prixWeekend(),
            )
            self.db.execute(query, params)
            return True
        except Exception as e:
            print(f"Erreur lors de la création: {e}")
            return False

    def get_by_id(self, id_panneau):
        """Get a panneau by ID"""
        try:
            query = "SELECT * FROM panneau WHERE idPanneau = ?"
            result = self.db.fetch_all(query, (id_panneau,))
            if result:
                row = result[0]
                panneau = Panneau(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                return panneau
            return None
        except Exception as e:
            print(f"Erreur lors de la lecture: {e}")
            return None

    def get_all(self):
        """Get all panneaux"""
        try:
            query = "SELECT * FROM panneau"
            result = self.db.fetch_all(query)
            panneaux = []
            for row in result:
                panneau = Panneau(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                panneaux.append(panneau)
            return panneaux
        except Exception as e:
            print(f"Erreur lors de la lecture: {e}")
            return []

    def update(self, panneau):
        """Update a panneau"""
        try:
            query = "UPDATE panneau SET nom = ?, rendement = ?, puissanceA = ?, puissanceB = ?, energie = ?, prixUnitaire = ?, prixWeekend = ? WHERE idPanneau = ?"
            params = (
                panneau.get_nom(),
                panneau.get_rendement(),
                panneau.get_puissanceA(),
                panneau.get_puissanceB(),
                panneau.get_energie(),
                panneau.get_prixUnitaire(),
                panneau.get_prixWeekend(),
                panneau.get_idPanneau(),
            )
            self.db.execute(query, params)
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour: {e}")
            return False

    def delete(self, id_panneau):
        """Delete a panneau"""
        try:
            query = "DELETE FROM panneau WHERE idPanneau = ?"
            self.db.execute(query, (id_panneau,))
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            return False
