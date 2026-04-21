class EnergieSolaire:
	def __init__(
		self,
		idEnergie=None,
		nom=None,
		pourcentage=None,
		heureDebut=None,
		heureFin=None,
		ref1=None,
	):
		self._idEnergie = idEnergie
		self._nom = nom
		self._pourcentage = pourcentage
		self._heureDebut = heureDebut
		self._heureFin = heureFin
		self._ref1 = ref1

	def get_idEnergie(self):
		return self._idEnergie

	def set_idEnergie(self, idEnergie):
		self._idEnergie = idEnergie

	def get_nom(self):
		return self._nom

	def set_nom(self, nom):
		self._nom = nom

	def get_pourcentage(self):
		return self._pourcentage

	def set_pourcentage(self, pourcentage):
		self._pourcentage = pourcentage

	def get_heureDebut(self):
		return self._heureDebut

	def set_heureDebut(self, heureDebut):
		self._heureDebut = heureDebut

	def get_heureFin(self):
		return self._heureFin

	def set_heureFin(self, heureFin):
		self._heureFin = heureFin

	def get_ref1(self):
		return self._ref1

	def set_ref1(self, ref1):
		self._ref1 = ref1
