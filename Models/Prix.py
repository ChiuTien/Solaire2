class Prix:
	def __init__(
		self,
		idPrix=None,
		prixOuvrable=None,
		prixWeekend=None,
		puissance=None,
	):
		self._idPrix = idPrix
		self._prixOuvrable = prixOuvrable
		self._prixWeekend = prixWeekend
		self._puissance = puissance

	def get_idPrix(self):
		return self._idPrix

	def set_idPrix(self, idPrix):
		self._idPrix = idPrix

	def get_prixOuvrable(self):
		return self._prixOuvrable

	def set_prixOuvrable(self, prixOuvrable):
		self._prixOuvrable = prixOuvrable

	def get_prixWeekend(self):
		return self._prixWeekend

	def set_prixWeekend(self, prixWeekend):
		self._prixWeekend = prixWeekend

	def get_puissance(self):
		return self._puissance

	def set_puissance(self, puissance):
		self._puissance = puissance
