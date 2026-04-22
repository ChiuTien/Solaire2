class HeurePointe:
	def __init__(self, id=None, heureDebut=None, heureFin=None, pourcentage=None):
		self._id = id
		self._heureDebut = heureDebut
		self._heureFin = heureFin
		self._pourcentage = pourcentage

	def get_id(self):
		return self._id

	def set_id(self, id):
		self._id = id

	def get_heureDebut(self):
		return self._heureDebut

	def set_heureDebut(self, heureDebut):
		self._heureDebut = heureDebut

	def get_heureFin(self):
		return self._heureFin

	def set_heureFin(self, heureFin):
		self._heureFin = heureFin

	def get_pourcentage(self):
		return self._pourcentage

	def set_pourcentage(self, pourcentage):
		self._pourcentage = pourcentage
