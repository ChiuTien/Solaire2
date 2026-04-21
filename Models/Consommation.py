class Consommation:
	def __init__(
		self,
		idConsommation=None,
		idAppareil=None,
		heureDebut=None,
		heureFin=None,
		consommation=None,
	):
		self._idConsommation = idConsommation
		self._idAppareil = idAppareil
		self._heureDebut = heureDebut
		self._heureFin = heureFin
		self._consommation = consommation

	def get_idConsommation(self):
		return self._idConsommation

	def set_idConsommation(self, idConsommation):
		self._idConsommation = idConsommation

	def get_idAppareil(self):
		return self._idAppareil

	def set_idAppareil(self, idAppareil):
		self._idAppareil = idAppareil

	def get_heureDebut(self):
		return self._heureDebut

	def set_heureDebut(self, heureDebut):
		self._heureDebut = heureDebut

	def get_heureFin(self):
		return self._heureFin

	def set_heureFin(self, heureFin):
		self._heureFin = heureFin

	def get_consommation(self):
		return self._consommation

	def set_consommation(self, consommation):
		self._consommation = consommation
