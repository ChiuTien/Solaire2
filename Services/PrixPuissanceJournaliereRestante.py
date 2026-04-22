from Services.PrixService import PrixService


def prix_achat(consommation_restante, energie_unitaire, prix_ouvrable, prix_weekend):
	"""Wrapper de compatibilite vers PrixService.prix_achat."""
	return PrixService.prix_achat(
		consommation_restante=consommation_restante,
		energie_unitaire=energie_unitaire,
		prix_ouvrable=prix_ouvrable,
		prix_weekend=prix_weekend,
	)
