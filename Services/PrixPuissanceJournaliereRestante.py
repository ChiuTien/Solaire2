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


def _to_minutes(hour_value):
	if hasattr(hour_value, "hour") and hasattr(hour_value, "minute"):
		return int(hour_value.hour) * 60 + int(hour_value.minute)

	if isinstance(hour_value, (int, float)):
		return int(float(hour_value) * 60)

	if isinstance(hour_value, str):
		normalized = hour_value.strip().lower().replace(" ", "")
		normalized = normalized.replace("h", ":")
		if normalized.endswith(":"):
			normalized = normalized[:-1] + ":00"

		if ":" in normalized:
			hour_part, minute_part = normalized.split(":", 1)
			return int(hour_part) * 60 + int(minute_part)

		return int(normalized) * 60

	raise ValueError(f"Format d'heure invalide: {hour_value}")


def _normalize_interval(start_minutes, end_minutes):
	if end_minutes <= start_minutes:
		end_minutes += 24 * 60
	return start_minutes, end_minutes


def _interval_overlap_minutes(start_a, end_a, start_b, end_b):
	left = max(start_a, start_b)
	right = min(end_a, end_b)
	if right <= left:
		return 0
	return right - left


def _energie_dans_plage(consommations, heure_debut, heure_fin):
	"""
	Retourne l'energie totale (consommation * heures) dans une plage horaire.
	"""
	window_start = _to_minutes(heure_debut)
	window_end = _to_minutes(heure_fin)
	window_start, window_end = _normalize_interval(window_start, window_end)

	# Deux fenetres pour couvrir les cas de passages a minuit.
	windows = [
		(window_start, window_end),
		(window_start + 24 * 60, window_end + 24 * 60),
	]

	energy = 0.0
	for conso in consommations or []:
		start = _to_minutes(conso.get_heureDebut())
		end = _to_minutes(conso.get_heureFin())
		start, end = _normalize_interval(start, end)

		for ws, we in windows:
			overlap = _interval_overlap_minutes(start, end, ws, we)
			if overlap > 0:
				duree_h = overlap / 60.0
				energy += float(conso.get_consommation()) * duree_h

	return energy


def calcul_augmentation(consommations, augmentations, energie_unitaire, prix_ouvrable, prix_weekend):
	if energie_unitaire == 0:
		raise ValueError("energie_unitaire doit etre different de 0")

	supplement_ouvrable = 0.0
	supplement_weekend = 0.0
	details = []

	for aug in augmentations or []:
		energie_aug = _energie_dans_plage(
			consommations,
			aug.get_heureDebut(),
			aug.get_heureFin(),
		)

		base_ouvrable = (energie_aug * float(prix_ouvrable) / float(energie_unitaire)) * 5
		base_weekend = (energie_aug * float(prix_weekend) / float(energie_unitaire)) * 2

		taux_ouvrable = float(aug.get_pourcentageOuvrable() or 0) / 100.0
		taux_weekend = float(aug.get_pourcentageWeekend() or 0) / 100.0

		sup_ouvrable = base_ouvrable * taux_ouvrable
		sup_weekend = base_weekend * taux_weekend

		supplement_ouvrable += sup_ouvrable
		supplement_weekend += sup_weekend

		details.append(
			f"{aug.get_heureDebut()}-{aug.get_heureFin()} | +{aug.get_pourcentageOuvrable()}% ouvrable, +{aug.get_pourcentageWeekend()}% weekend"
		)

	return supplement_ouvrable, supplement_weekend, details
