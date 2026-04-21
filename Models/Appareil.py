class Appareil:
	def __init__(self, idAppareil=None, nom=None):
		self._idAppareil = idAppareil
		self._nom = nom

	def get_idAppareil(self):
		return self._idAppareil

	def set_idAppareil(self, idAppareil):
		self._idAppareil = idAppareil

	def get_nom(self):
		return self._nom

	def set_nom(self, nom):
		self._nom = nom
