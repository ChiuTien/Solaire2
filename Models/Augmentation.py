class Augmentation:
	def __init__(
		self,
		idAugmentation=None,
		pourcentageOuvrable=None,
		pourcentageWeekend=None,
		heureDebut=None,
		heureFin=None,
	):
		self._idAugmentation = idAugmentation
		self._pourcentageOuvrable = pourcentageOuvrable
		self._pourcentageWeekend = pourcentageWeekend
		self._heureDebut = heureDebut
		self._heureFin = heureFin

	def get_idAugmentation(self):
		return self._idAugmentation

	def set_idAugmentation(self, idAugmentation):
		self._idAugmentation = idAugmentation

	def get_pourcentageOuvrable(self):
		return self._pourcentageOuvrable

	def set_pourcentageOuvrable(self, pourcentageOuvrable):
		self._pourcentageOuvrable = pourcentageOuvrable

	def get_pourcentageWeekend(self):
		return self._pourcentageWeekend

	def set_pourcentageWeekend(self, pourcentageWeekend):
		self._pourcentageWeekend = pourcentageWeekend

	def get_heureDebut(self):
		return self._heureDebut

	def set_heureDebut(self, heureDebut):
		self._heureDebut = heureDebut

	def get_heureFin(self):
		return self._heureFin

	def set_heureFin(self, heureFin):
		self._heureFin = heureFin
