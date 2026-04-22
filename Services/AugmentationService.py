from Models.Augmentation import Augmentation
from Repositories.AugmentationRepository import AugmentationRepository


class AugmentationService:
	def __init__(self, repository=None):
		self.repo = repository if repository is not None else AugmentationRepository()

	@staticmethod
	def _validate_values(pourcentage_ouvrable, pourcentage_weekend, heure_debut, heure_fin):
		if pourcentage_ouvrable is None or pourcentage_weekend is None:
			raise ValueError("pourcentageOuvrable et pourcentageWeekend sont obligatoires")
		if not heure_debut or not heure_fin:
			raise ValueError("heureDebut et heureFin sont obligatoires")

		pourcentage_ouvrable = float(pourcentage_ouvrable)
		pourcentage_weekend = float(pourcentage_weekend)

		if pourcentage_ouvrable < 0 or pourcentage_weekend < 0:
			raise ValueError("Les pourcentages ne peuvent pas etre negatifs")

		return pourcentage_ouvrable, pourcentage_weekend, heure_debut, heure_fin

	def create_augmentation(self, pourcentage_ouvrable, pourcentage_weekend, heure_debut, heure_fin):
		pourcentage_ouvrable, pourcentage_weekend, heure_debut, heure_fin = self._validate_values(
			pourcentage_ouvrable,
			pourcentage_weekend,
			heure_debut,
			heure_fin,
		)
		augmentation = Augmentation(
			pourcentageOuvrable=pourcentage_ouvrable,
			pourcentageWeekend=pourcentage_weekend,
			heureDebut=heure_debut,
			heureFin=heure_fin,
		)
		return self.repo.create(augmentation)

	def get_augmentation_by_id(self, id_augmentation):
		return self.repo.get_by_id(id_augmentation)

	def get_all_augmentations(self):
		return self.repo.get_all()

	def update_augmentation(self, id_augmentation, pourcentage_ouvrable, pourcentage_weekend, heure_debut, heure_fin):
		pourcentage_ouvrable, pourcentage_weekend, heure_debut, heure_fin = self._validate_values(
			pourcentage_ouvrable,
			pourcentage_weekend,
			heure_debut,
			heure_fin,
		)
		augmentation = Augmentation(
			idAugmentation=id_augmentation,
			pourcentageOuvrable=pourcentage_ouvrable,
			pourcentageWeekend=pourcentage_weekend,
			heureDebut=heure_debut,
			heureFin=heure_fin,
		)
		return self.repo.update(augmentation)

	def delete_augmentation(self, id_augmentation):
		return self.repo.delete(id_augmentation)
