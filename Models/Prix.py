class Prix:
	def __init__(self, id=None, prixUnitaire=None, prixWeekend=None, EnergieSolaire=None):
		self._id = id
		self._prixUnitaire = prixUnitaire
		self._prixWeekend = prixWeekend
		self._EnergieSolaire = EnergieSolaire

	def get_id(self):
		return self._id

	def set_id(self, id):
		self._id = id

	def get_prixUnitaire(self):
		return self._prixUnitaire

	def set_prixUnitaire(self, prixUnitaire):
		self._prixUnitaire = prixUnitaire

	def get_prixWeekend(self):
		return self._prixWeekend

	def set_prixWeekend(self, prixWeekend):
		self._prixWeekend = prixWeekend

	def get_EnergieSolaire(self):
		return self._EnergieSolaire

	def set_EnergieSolaire(self, EnergieSolaire):
		self._EnergieSolaire = EnergieSolaire
