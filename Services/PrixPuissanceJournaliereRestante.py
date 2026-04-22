from Services.PrixService import PrixService


def prix_achat(consommation_restante, energie_unitaire, prix_ouvrable=None, prix_weekend=None):
	"""
	Retourne deux montants (ouvrable, weekend) sous forme de float.

	Formules:
	- ouvrable = consommation_restante * prix_ouvrable / energie_unitaire
	- weekend = consommation_restante * prix_weekend / energie_unitaire
	"""
	if prix_ouvrable is None or prix_weekend is None:
		prix_data = PrixService().get_latest_prix()
		if prix_data is None:
			raise ValueError("Aucun prix en base. Veuillez inserer une ligne dans la table prix.")

		prix_ouvrable = prix_data.get_prixOuvrable()
		prix_weekend = prix_data.get_prixWeekend()

	if prix_ouvrable == 0 or prix_weekend == 0:
		raise ValueError("prix_ouvrable et prix_weekend doivent etre differents de 0")

	if energie_unitaire == 0:
		raise ValueError("energie_unitaire doit etre different de 0")

	journalier = (float(consommation_restante) * float(prix_ouvrable) /float(energie_unitaire) )*5
	weekend = (float(consommation_restante) *  float(prix_weekend) /float(energie_unitaire) )*2

	return [journalier, weekend]
