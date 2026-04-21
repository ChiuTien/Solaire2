from Connection.Connexion import SQLServerDB
from Models.EnergieSolaire import EnergieSolaire


class EnergieSolaireRepository:
    def __init__(self):
        self.db = SQLServerDB()

    def create(self, energie_solaire):
        """Insert a new energie solaire"""
        try:
            query = "INSERT INTO energieSolaire (nom, pourcentage, heureDebut, heureFin, ref1) VALUES (?, ?, ?, ?, ?)"
            params = (
                energie_solaire.get_nom(),
                energie_solaire.get_pourcentage(),
                energie_solaire.get_heureDebut(),
                energie_solaire.get_heureFin(),
                energie_solaire.get_ref1(),
            )
            self.db.execute(query, params)
            return True
        except Exception as e:
            print(f"Erreur lors de la création: {e}")
            return False

    def get_by_id(self, id_energie):
        """Get an energie solaire by ID"""
        try:
            query = "SELECT * FROM energieSolaire WHERE idEnergie = ?"
            result = self.db.fetch_all(query, (id_energie,))
            if result:
                row = result[0]
                energie_solaire = EnergieSolaire(row[0], row[1], row[2], row[3], row[4], row[5])
                return energie_solaire
            return None
        except Exception as e:
            print(f"Erreur lors de la lecture: {e}")
            return None

    def get_all(self):
        """Get all energies solaires"""
        try:
            query = "SELECT * FROM energieSolaire"
            result = self.db.fetch_all(query)
            energies = []
            for row in result:
                energie_solaire = EnergieSolaire(row[0], row[1], row[2], row[3], row[4], row[5])
                energies.append(energie_solaire)
            return energies
        except Exception as e:
            print(f"Erreur lors de la lecture: {e}")
            return []

    def update(self, energie_solaire):
        """Update an energie solaire"""
        try:
            query = "UPDATE energieSolaire SET nom = ?, pourcentage = ?, heureDebut = ?, heureFin = ?, ref1 = ? WHERE idEnergie = ?"
            params = (
                energie_solaire.get_nom(),
                energie_solaire.get_pourcentage(),
                energie_solaire.get_heureDebut(),
                energie_solaire.get_heureFin(),
                energie_solaire.get_ref1(),
                energie_solaire.get_idEnergie(),
            )
            self.db.execute(query, params)
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour: {e}")
            return False

    def delete(self, id_energie):
        """Delete an energie solaire"""
        try:
            query = "DELETE FROM energieSolaire WHERE idEnergie = ?"
            self.db.execute(query, (id_energie,))
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            return False
