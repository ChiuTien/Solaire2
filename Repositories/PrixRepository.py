from Connection.Connexion import SQLServerDB
from Models.Prix import Prix


class PrixRepository:
    def __init__(self):
        self.db = SQLServerDB()
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        """Create table prix if it does not exist in the current database."""
        try:
            query = """
                IF OBJECT_ID('dbo.prix', 'U') IS NULL
                BEGIN
                    CREATE TABLE dbo.prix (
                        idPrix INT IDENTITY(1,1) PRIMARY KEY,
                        prixOuvrable FLOAT,
                        prixWeekend FLOAT,
                        puissance FLOAT
                    )
                END
            """
            self.db.execute(query)
        except Exception as e:
            print(f"Erreur lors de l'initialisation de la table prix: {e}")

    def create(self, prix):
        """Insert a new prix"""
        try:
            query = "INSERT INTO dbo.prix (prixOuvrable, prixWeekend, puissance) VALUES (?, ?, ?)"
            params = (
                prix.get_prixOuvrable(),
                prix.get_prixWeekend(),
                prix.get_puissance(),
            )
            self.db.execute(query, params)
            return True
        except Exception as e:
            print(f"Erreur lors de la creation: {e}")
            return False

    def get_by_id(self, id_prix):
        """Get a prix by ID"""
        try:
            query = "SELECT * FROM dbo.prix WHERE idPrix = ?"
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
            query = "SELECT * FROM dbo.prix"
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
            query = "UPDATE dbo.prix SET prixOuvrable = ?, prixWeekend = ?, puissance = ? WHERE idPrix = ?"
            params = (
                prix.get_prixOuvrable(),
                prix.get_prixWeekend(),
                prix.get_puissance(),
                prix.get_idPrix(),
            )
            self.db.execute(query, params)
            return True
        except Exception as e:
            print(f"Erreur lors de la mise a jour: {e}")
            return False

    def delete(self, id_prix):
        """Delete a prix"""
        try:
            query = "DELETE FROM dbo.prix WHERE idPrix = ?"
            self.db.execute(query, (id_prix,))
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            return False
