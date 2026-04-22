from Models.Prix import Prix
from Repositories.PrixRepository import PrixRepository


class PrixService:
	def __init__(self, repository=None):
		self.repo = repository if repository is not None else PrixRepository()

	@staticmethod
	def _validate_values(prix_ouvrable, prix_weekend, puissance):
		if prix_ouvrable is None or prix_weekend is None or puissance is None:
			raise ValueError("prixOuvrable, prixWeekend et puissance sont obligatoires")

		prix_ouvrable = float(prix_ouvrable)
		prix_weekend = float(prix_weekend)
		puissance = float(puissance)

		if prix_ouvrable < 0 or prix_weekend < 0 or puissance < 0:
			raise ValueError("Les valeurs ne peuvent pas etre negatives")

		return prix_ouvrable, prix_weekend, puissance

	def create_prix(self, prix_ouvrable, prix_weekend, puissance):
		prix_ouvrable, prix_weekend, puissance = self._validate_values(
			prix_ouvrable,
			prix_weekend,
			puissance,
		)
		prix = Prix(
			prixOuvrable=prix_ouvrable,
			prixWeekend=prix_weekend,
			puissance=puissance,
		)
		return self.repo.create(prix)

	def get_prix_by_id(self, id_prix):
		return self.repo.get_by_id(id_prix)

	def get_all_prix(self):
		return self.repo.get_all()

	def update_prix(self, id_prix, prix_ouvrable, prix_weekend, puissance):
		prix_ouvrable, prix_weekend, puissance = self._validate_values(
			prix_ouvrable,
			prix_weekend,
			puissance,
		)
		prix = Prix(
			idPrix=id_prix,
			prixOuvrable=prix_ouvrable,
			prixWeekend=prix_weekend,
			puissance=puissance,
		)
		return self.repo.update(prix)

	def delete_prix(self, id_prix):
		return self.repo.delete(id_prix)

	def calculer_montant(self, consommation_restante, prix: Prix, est_weekend=False):
		"""
		Calcule un montant selon la consommation restante et le type de jour.
		"""
		if prix is None:
			raise ValueError("L'objet prix est obligatoire")

		base = prix.get_prixWeekend() if est_weekend else prix.get_prixOuvrable()
		if base is None or prix.get_puissance() in (None, 0):
			raise ValueError("prix et puissance doivent etre definis, puissance != 0")

		return float(consommation_restante) * float(base) / float(prix.get_puissance())
