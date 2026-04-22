from datetime import time

from Models.Consommation import Consommation


class ConsommationService:
	@staticmethod
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

	@staticmethod
	def _minutes_to_string(total_minutes):
		value = total_minutes % (24 * 60)
		hours = value // 60
		minutes = value % 60
		if minutes == 0:
			return str(hours)
		return f"{hours}:{minutes:02d}"

	@staticmethod
	def _normalize_interval(start_minutes, end_minutes):
		# Si la fin <= debut, la plage traverse minuit.
		if end_minutes <= start_minutes:
			end_minutes += 24 * 60
		return start_minutes, end_minutes

	@staticmethod
	def _intersections_with_windows(start, end, windows):
		intersections = []
		for window_start, window_end in windows:
			left = max(start, window_start)
			right = min(end, window_end)
			if right > left:
				intersections.append((left, right))
		return intersections

	@staticmethod
	def _build_output(consommation_source, segments):
		result = []
		for seg_start, seg_end in segments:
			result.append(
				Consommation(
					idConsommation=None,
					idAppareil=consommation_source.get_idAppareil(),
					heureDebut=ConsommationService._minutes_to_string(seg_start),
					heureFin=ConsommationService._minutes_to_string(seg_end),
					consommation=consommation_source.get_consommation(),
				)
			)
		return result

	@staticmethod
	def retourner_consommation_journee(consommations, heure_debut_jour=6, heure_fin_jour=19):
		"""
		Retourne les portions de consommation entre 6h et 19h.
		Exemple: 17-6 => 17-19 uniquement.
		"""
		if not consommations:
			return []

		day_start = ConsommationService._to_minutes(heure_debut_jour)
		day_end = ConsommationService._to_minutes(heure_fin_jour)
		if day_end <= day_start:
			raise ValueError("La plage journee doit avoir heure_fin > heure_debut")

		# Deux fenetres couvrent une timeline etendue jusqu'a 48h.
		day_windows = [
			(day_start, day_end),
			(day_start + 24 * 60, day_end + 24 * 60),
		]

		result = []
		for conso in consommations:
			start = ConsommationService._to_minutes(conso.get_heureDebut())
			end = ConsommationService._to_minutes(conso.get_heureFin())
			start, end = ConsommationService._normalize_interval(start, end)

			segments = ConsommationService._intersections_with_windows(start, end, day_windows)
			result.extend(ConsommationService._build_output(conso, segments))

		return result

	@staticmethod
	def retourner_consommation_soiree(consommations, heure_debut_soiree=19, heure_fin_soiree=6):
		"""
		Retourne les portions de consommation sur la soiree/nuit (19h -> 6h).
		Exemple: 17-6 => 19-6.
		"""
		if not consommations:
			return []

		evening_start = ConsommationService._to_minutes(heure_debut_soiree)
		evening_end = ConsommationService._to_minutes(heure_fin_soiree)
		if evening_end <= evening_start:
			evening_end += 24 * 60

		evening_windows = [
			(evening_start, evening_end),
			(evening_start + 24 * 60, evening_end + 24 * 60),
		]

		result = []
		for conso in consommations:
			start = ConsommationService._to_minutes(conso.get_heureDebut())
			end = ConsommationService._to_minutes(conso.get_heureFin())
			start, end = ConsommationService._normalize_interval(start, end)

			segments = ConsommationService._intersections_with_windows(start, end, evening_windows)
			result.extend(ConsommationService._build_output(conso, segments))

		return result
