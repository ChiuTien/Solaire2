class Batterie:
	def __init__(
		self,
		idBatterie=None,
		nom=None,
		rendement=None,
		capacite=None,
		chargeDebut=None,
		chargeFin=None,
	):
		self._idBatterie = idBatterie
		self._nom = nom
		self._rendement = rendement
		self._capacite = capacite
		self._chargeDebut = chargeDebut
		self._chargeFin = chargeFin

	def get_idBatterie(self):
		return self._idBatterie

	def set_idBatterie(self, idBatterie):
		self._idBatterie = idBatterie

	def get_nom(self):
		return self._nom

	def set_nom(self, nom):
		self._nom = nom

	def get_rendement(self):
		return self._rendement

	def set_rendement(self, rendement):
		self._rendement = rendement

	def get_capacite(self):
		return self._capacite

	def set_capacite(self, capacite):
		self._capacite = capacite

	def get_chargeDebut(self):
		return self._chargeDebut

	def set_chargeDebut(self, chargeDebut):
		self._chargeDebut = chargeDebut

	def get_chargeFin(self):
		return self._chargeFin

	def set_chargeFin(self, chargeFin):
		self._chargeFin = chargeFin
