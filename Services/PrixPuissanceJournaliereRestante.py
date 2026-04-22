from datetime import time


def _to_minutes(hour_value):
	if isinstance(hour_value, time):
		return hour_value.hour * 60 + hour_value.minute

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


def _overlap_minutes(start_a, end_a, start_b, end_b):
	left = max(start_a, start_b)
	right = min(end_a, end_b)
	return max(0, right - left)


def _build_shifted_windows(start, end):
	return [
		(start, end),
		(start + 24 * 60, end + 24 * 60),
	]


def _energie_sur_heure_pointe(consommations, heure_pointes):
	if not consommations or not heure_pointes:
		return 0.0

	energie_totale = 0.0

	for conso in consommations:
		conso_start = _to_minutes(conso.get_heureDebut())
		conso_end = _to_minutes(conso.get_heureFin())
		conso_start, conso_end = _normalize_interval(conso_start, conso_end)
		conso_windows = _build_shifted_windows(conso_start, conso_end)
		puissance = float(conso.get_consommation() or 0.0)

		for hp in heure_pointes:
			hp_start = _to_minutes(hp.get_heureDebut())
			hp_end = _to_minutes(hp.get_heureFin())
			hp_start, hp_end = _normalize_interval(hp_start, hp_end)
			hp_windows = _build_shifted_windows(hp_start, hp_end)
			pourcentage = float(hp.get_pourcentage() or 0.0)

			overlap_total = 0
			for c_start, c_end in conso_windows:
				for h_start, h_end in hp_windows:
					overlap_total += _overlap_minutes(c_start, c_end, h_start, h_end)

			overlap_heures = overlap_total / 60.0
			if overlap_heures > 0:
				energie_totale += pourcentage * (puissance * overlap_heures)

	return energie_totale


def prix_achat(
	consommation_restante,
	energie_unitaire,
	prix_journaliere,
	prix_weekend,
	consommations_journee=None,
	heure_pointes=None,
):
	"""
	Calcule le prix total achat (journalier + weekend) avec majoration heure de pointe.

	Majoration appliquee:
	prix_total + somme(heure_pointe.pourcentage * (conso_sur_tranche * prix / energie_unitaire))
	"""
	if prix_journaliere == 0 or prix_weekend == 0 or energie_unitaire == 0:
		raise ValueError("prix_journaliere, prix_weekend et energie_unitaire doivent etre differents de 0")

	base_journalier = (float(consommation_restante) * float(prix_journaliere) / float(energie_unitaire)) * 5
	base_weekend = (float(consommation_restante) * float(prix_weekend) / float(energie_unitaire)) * 2

	energie_majoree = _energie_sur_heure_pointe(consommations_journee or [], heure_pointes or [])
	majoration_journalier = (energie_majoree * float(prix_journaliere) / float(energie_unitaire)) * 5
	majoration_weekend = (energie_majoree * float(prix_weekend) / float(energie_unitaire)) * 2

	journalier = base_journalier + majoration_journalier
	weekend = base_weekend + majoration_weekend

	return [journalier, weekend]



