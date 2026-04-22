from Connection.Connexion import SQLServerDB
from Models.Prix import Prix


class PrixRepository:
    def __init__(self):
        self.db = SQLServerDB()
        self._ensure_table()

    def _ensure_table(self):
        try:
            query = """
            IF OBJECT_ID('dbo.PRIX', 'U') IS NULL
            BEGIN
                CREATE TABLE dbo.PRIX (
                    idPrix INT IDENTITY(1,1) PRIMARY KEY,
                    prixOuvrable FLOAT,
                    prixWeekend FLOAT,
                    puissance FLOAT
                );
            END
            """
            self.db.execute(query)
        except Exception as e:
            print(f"Erreur lors de la verification/creation de PRIX: {e}")

    def get_all(self):
        try:
            query = "SELECT idPrix, prixOuvrable, prixWeekend, puissance FROM dbo.PRIX ORDER BY idPrix DESC"
            rows = self.db.fetch_all(query)
            prix_list = []
            for row in rows:
                prix_list.append(Prix(row[0], row[1], row[2], row[3]))
            return prix_list
        except Exception as e:
            print(f"Erreur lors de la lecture de la liste des prix: {e}")
            return []

    def get_latest(self):
        try:
            query = "SELECT TOP 1 idPrix, prixOuvrable, prixWeekend, puissance FROM dbo.PRIX ORDER BY idPrix DESC"
            result = self.db.fetch_all(query)
            if not result:
                return None

            row = result[0]
            return Prix(row[0], row[1], row[2], row[3])
        except Exception as e:
            print(f"Erreur lors de la lecture des prix: {e}")
            return None

    def get_by_id(self, id_prix):
        try:
            query = "SELECT idPrix, prixOuvrable, prixWeekend, puissance FROM dbo.PRIX WHERE idPrix = ?"
            result = self.db.fetch_all(query, (id_prix,))
            if not result:
                return None

            row = result[0]
            return Prix(row[0], row[1], row[2], row[3])
        except Exception as e:
            print(f"Erreur lors de la lecture du prix: {e}")
            return None

    def create(self, prix):
        try:
            query = "INSERT INTO dbo.PRIX (prixOuvrable, prixWeekend, puissance) VALUES (?, ?, ?)"
            self.db.execute(
                query,
                (prix.get_prixOuvrable(), prix.get_prixWeekend(), prix.get_puissance()),
            )
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des prix: {e}")
            return False

    def update(self, prix):
        try:
            query = "UPDATE dbo.PRIX SET prixOuvrable = ?, prixWeekend = ?, puissance = ? WHERE idPrix = ?"
            self.db.execute(
                query,
                (
                    prix.get_prixOuvrable(),
                    prix.get_prixWeekend(),
                    prix.get_puissance(),
                    prix.get_idPrix(),
                ),
            )
            return True
        except Exception as e:
            print(f"Erreur lors de la mise a jour des prix: {e}")
            return False

    def delete(self, id_prix):
        try:
            query = "DELETE FROM dbo.PRIX WHERE idPrix = ?"
            self.db.execute(query, (id_prix,))
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression des prix: {e}")
            return False

    def save(self, prix_ouvrable, prix_weekend, puissance):
        # Compatibilite avec l'ancien appel save(prix_ouvrable, prix_weekend, puissance).
        return self.create(Prix(None, prix_ouvrable, prix_weekend, puissance))
