from Connection.Connexion import SQLServerDB
from Models.Augmentation import Augmentation


class AugmentationRepository:
    def __init__(self):
        self.db = SQLServerDB()
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        """Create table augmentation if it does not exist in the current database."""
        try:
            query = """
                IF OBJECT_ID('dbo.augmentation', 'U') IS NULL
                BEGIN
                    CREATE TABLE dbo.augmentation (
                        idAugmentation INT IDENTITY(1,1) PRIMARY KEY,
                        pourcentageOuvrable FLOAT,
                        pourcentageWeekend FLOAT,
                        heureDebut TIME,
                        heureFin TIME
                    )
                END

                IF COL_LENGTH('dbo.augmentation', 'heureDebut') IS NULL
                BEGIN
                    ALTER TABLE dbo.augmentation ADD heureDebut TIME NULL
                END

                IF COL_LENGTH('dbo.augmentation', 'heureFin') IS NULL
                BEGIN
                    ALTER TABLE dbo.augmentation ADD heureFin TIME NULL
                END
            """
            self.db.execute(query)
        except Exception as e:
            print(f"Erreur lors de l'initialisation de la table augmentation: {e}")

    def create(self, augmentation):
        """Insert a new augmentation"""
        try:
            query = "INSERT INTO dbo.augmentation (pourcentageOuvrable, pourcentageWeekend, heureDebut, heureFin) VALUES (?, ?, ?, ?)"
            params = (
                augmentation.get_pourcentageOuvrable(),
                augmentation.get_pourcentageWeekend(),
                augmentation.get_heureDebut(),
                augmentation.get_heureFin(),
            )
            self.db.execute(query, params)
            return True
        except Exception as e:
            print(f"Erreur lors de la creation: {e}")
            return False

    def get_by_id(self, id_augmentation):
        """Get an augmentation by ID"""
        try:
            query = "SELECT * FROM dbo.augmentation WHERE idAugmentation = ?"
            result = self.db.fetch_all(query, (id_augmentation,))
            if result:
                row = result[0]
                augmentation = Augmentation(row[0], row[1], row[2], row[3], row[4])
                return augmentation
            return None
        except Exception as e:
            print(f"Erreur lors de la lecture: {e}")
            return None

    def get_all(self):
        """Get all augmentations"""
        try:
            query = "SELECT * FROM dbo.augmentation"
            result = self.db.fetch_all(query)
            augmentations = []
            for row in result:
                augmentation = Augmentation(row[0], row[1], row[2], row[3], row[4])
                augmentations.append(augmentation)
            return augmentations
        except Exception as e:
            print(f"Erreur lors de la lecture: {e}")
            return []

    def update(self, augmentation):
        """Update an augmentation"""
        try:
            query = "UPDATE dbo.augmentation SET pourcentageOuvrable = ?, pourcentageWeekend = ?, heureDebut = ?, heureFin = ? WHERE idAugmentation = ?"
            params = (
                augmentation.get_pourcentageOuvrable(),
                augmentation.get_pourcentageWeekend(),
                augmentation.get_heureDebut(),
                augmentation.get_heureFin(),
                augmentation.get_idAugmentation(),
            )
            self.db.execute(query, params)
            return True
        except Exception as e:
            print(f"Erreur lors de la mise a jour: {e}")
            return False

    def delete(self, id_augmentation):
        """Delete an augmentation"""
        try:
            query = "DELETE FROM dbo.augmentation WHERE idAugmentation = ?"
            self.db.execute(query, (id_augmentation,))
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            return False
