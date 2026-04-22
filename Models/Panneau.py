class Panneau:
	def __init__(
		self,
		idPanneau=None,
		nom=None,
		rendement=None,
		puissanceA=None,
		puissanceB=None,
		energie=None,
		prixUnitaire=None,
		prixWeekend=None,
	):
		self._idPanneau = idPanneau
		self._nom = nom
		self._rendement = rendement
		self._puissanceA = puissanceA
		self._puissanceB = puissanceB
		self._energie = energie
		self._prixUnitaire = prixUnitaire
		self._prixWeekend = prixWeekend

	def get_idPanneau(self):
		return self._idPanneau

	def set_idPanneau(self, idPanneau):
		self._idPanneau = idPanneau

	def get_nom(self):
		return self._nom

	def set_nom(self, nom):
		self._nom = nom

	def get_rendement(self):
		return self._rendement

	def set_rendement(self, rendement):
		self._rendement = rendement

	def get_puissanceA(self):
		return self._puissanceA

	def set_puissanceA(self, puissanceA):
		self._puissanceA = puissanceA

	def get_puissanceB(self):
		return self._puissanceB

	def set_puissanceB(self, puissanceB):
		self._puissanceB = puissanceB

	def get_energie(self):
		return self._energie

	def set_energie(self, energie):
		self._energie = energie

	def get_prixUnitaire(self):
		return self._prixUnitaire

	def set_prixUnitaire(self, prixUnitaire):
		self._prixUnitaire = prixUnitaire

	def get_prixWeekend(self):
		return self._prixWeekend

	def set_prixWeekend(self, prixWeekend):
		self._prixWeekend = prixWeekend
