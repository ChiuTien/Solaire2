from Connection.Connexion import SQLServerDB
from Models.Batterie import Batterie


class BatterieRepository:
    def __init__(self):
        self.db = SQLServerDB()

    def create(self, batterie):
        """Insert a new batterie"""
        try:
            query = "INSERT INTO batterie (nom, rendement, capacite, chargeDebut, chargeFin) VALUES (?, ?, ?, ?, ?)"
            params = (
                batterie.get_nom(),
                batterie.get_rendement(),
                batterie.get_capacite(),
                batterie.get_chargeDebut(),
                batterie.get_chargeFin(),
            )
            self.db.execute(query, params)
            return True
        except Exception as e:
            print(f"Erreur lors de la création: {e}")
            return False

    def get_by_id(self, id_batterie):
        """Get a batterie by ID"""
        try:
            query = "SELECT * FROM batterie WHERE idBatterie = ?"
            result = self.db.fetch_all(query, (id_batterie,))
            if result:
                row = result[0]
                batterie = Batterie(row[0], row[1], row[2], row[3], row[4], row[5])
                return batterie
            return None
        except Exception as e:
            print(f"Erreur lors de la lecture: {e}")
            return None

    def get_all(self):
        """Get all batteries"""
        try:
            query = "SELECT * FROM batterie"
            result = self.db.fetch_all(query)
            batteries = []
            for row in result:
                batterie = Batterie(row[0], row[1], row[2], row[3], row[4], row[5])
                batteries.append(batterie)
            return batteries
        except Exception as e:
            print(f"Erreur lors de la lecture: {e}")
            return []

    def update(self, batterie):
        """Update a batterie"""
        try:
            query = "UPDATE batterie SET nom = ?, rendement = ?, capacite = ?, chargeDebut = ?, chargeFin = ? WHERE idBatterie = ?"
            params = (
                batterie.get_nom(),
                batterie.get_rendement(),
                batterie.get_capacite(),
                batterie.get_chargeDebut(),
                batterie.get_chargeFin(),
                batterie.get_idBatterie(),
            )
            self.db.execute(query, params)
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour: {e}")
            return False

    def delete(self, id_batterie):
        """Delete a batterie"""
        try:
            query = "DELETE FROM batterie WHERE idBatterie = ?"
            self.db.execute(query, (id_batterie,))
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            return False
