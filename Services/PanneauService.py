from datetime import time

from Models.Consommation import Consommation


class PanneauService:
	@staticmethod
	def _to_minutes(hour_value):
		"""Convertit une heure en minutes (ex: 6, '6h', '06:30')."""
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
		"""Convertit des minutes vers HH:MM (ou HH si minute = 00)."""
		hours = total_minutes // 60
		minutes = total_minutes % 60
		if minutes == 0:
			return str(hours)
		return f"{hours}:{minutes:02d}"

	@staticmethod
	def calculer_consommation_fusionnee(consommations):
		"""
		Fusionne les plages de consommation en additionnant les chevauchements.

		Parametre:
			consommations: liste d'objets Consommation

		Retour:
			Liste d'objets Consommation fusionnes
		"""
		if not consommations:
			return []

		events = []
		id_appareil = consommations[0].get_idAppareil() if consommations else None

		for conso in consommations:
			debut = conso.get_heureDebut()
			fin = conso.get_heureFin()
			puissance = conso.get_consommation()

			debut_minutes = PanneauService._to_minutes(debut)
			fin_minutes = PanneauService._to_minutes(fin)

			if fin_minutes <= debut_minutes:
				raise ValueError("L'heure de fin doit etre superieure a l'heure de debut")

			events.append((debut_minutes, float(puissance)))
			events.append((fin_minutes, -float(puissance)))

		events.sort(key=lambda item: (item[0], -item[1]))
		points = sorted({event[0] for event in events})

		delta_by_time = {}
		for t, delta in events:
			delta_by_time[t] = delta_by_time.get(t, 0) + delta

		resultat = []
		puissance_courante = 0.0

		for i in range(len(points) - 1):
			current_time = points[i]
			next_time = points[i + 1]

			puissance_courante += delta_by_time.get(current_time, 0)
			if puissance_courante <= 0:
				continue

			valeur = (
				int(puissance_courante)
				if puissance_courante.is_integer()
				else puissance_courante
			)

			resultat.append(
				Consommation(
					idConsommation=None,
					idAppareil=id_appareil,
					heureDebut=PanneauService._minutes_to_string(current_time),
					heureFin=PanneauService._minutes_to_string(next_time),
					consommation=valeur,
				)
			)

		return resultat

	@staticmethod
	def retourner_pic(consommations):
		"""
		Retourne la consommation de pic (valeur maximale) apres fusion.

		Retour:
			Objet Consommation avec la puissance maximale, ou None si vide.
		"""
		consommations_fusionnees = PanneauService.calculer_consommation_fusionnee(consommations)
		if not consommations_fusionnees:
			return None

		return max(consommations_fusionnees, key=lambda c: c.get_consommation())

	@staticmethod
	def _duree_heures(heure_debut, heure_fin):
		"""Retourne la duree en heures, avec gestion du passage a minuit."""
		debut = PanneauService._to_minutes(heure_debut)
		fin = PanneauService._to_minutes(heure_fin)
		if fin <= debut:
			fin += 24 * 60
		return (fin - debut) / 60.0

	@staticmethod
	def calcul_puissance_scolaire(consommation_journaliere, energie_solaires):
		"""
		Calcule la puissance solaire disponible selon les tranches EnergieSolaire.

		Formule:
			pic(consommation_journaliere) * somme(duree_tranche * pourcentage_tranche)
		"""
		if not consommation_journaliere or not energie_solaires:
			return 0

		duree_ponderee = 0.0
		for energie in energie_solaires:
			duree = PanneauService._duree_heures(
				energie.get_heureDebut(),
				energie.get_heureFin(),
			)
			pourcentage = float(energie.get_pourcentage() or 0)
			duree_ponderee += duree * pourcentage

		pic = PanneauService.retourner_pic(consommation_journaliere)
		if pic is None:
			return 0

		return pic.get_consommation() * duree_ponderee

	@staticmethod
	def calcul_puissance_solaire(consommation_journaliere, energie_solaires):
		"""Alias de compatibilite pour le nom correct 'solaire'."""
		return PanneauService.calcul_puissance_scolaire(consommation_journaliere, energie_solaires)

	@staticmethod
	def calcul_puissance_restante(consommation_journaliere, energie_solaires):
		"""
		Calcule la puissance restante:
			puissance_solaire_disponible - consommation_totale_journee
		"""
		somme_consommation = 0.0
		for conso in consommation_journaliere or []:
			duree = PanneauService._duree_heures(conso.get_heureDebut(), conso.get_heureFin())
			somme_consommation += float(conso.get_consommation()) * duree

		puissance_solaire = PanneauService.calcul_puissance_scolaire(
			consommation_journaliere,
			energie_solaires,
		)

		return puissance_solaire - somme_consommation
