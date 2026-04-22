def prix_achat(consommation_restante, energie_unitaire, prix_journaliere, prix_weekend):
	"""
	Retourne deux montants (journalier, weekend) sous forme de float.

	Formules:
	- journalier = consommation_restante * energie_unitaire / prix_journaliere
	- weekend = consommation_restante * energie_unitaire / prix_weekend
	"""
	if prix_journaliere == 0 or prix_weekend == 0:
		raise ValueError("prix_journaliere et prix_weekend doivent etre differents de 0")

	journalier = (float(consommation_restante) * float(prix_journaliere) /float(energie_unitaire) )*5
	weekend = (float(consommation_restante) *  float(prix_weekend) /float(energie_unitaire) )*2

	return [journalier, weekend]
