from Models.Consommation import Consommation
from Services.PanneauService import PanneauService

consommations = [
    Consommation(None, 1, "8h", "12h", 55),
    Consommation(None, 1, "10", "14", 75),
    Consommation(None, 1, "6", "17", 120),
    Consommation(None, 1, "17", "19", 10),
    Consommation(None, 1, "17", "19", 55),
    Consommation(None, 1, "19", "6", 10),
    Consommation(None, 1, "19", "6", 120),
    Consommation(None, 1, "19", "23", 10)
#  Consommation(None, 1, "6", "12", 100),
]

nouvelle_liste = PanneauService.calculer_consommation_fusionnee(consommations)

for c in nouvelle_liste:
    print(c.get_heureDebut(), c.get_heureFin(), c.get_consommation())
# 6 7 500
# 7 9 800
# 9 10 500
# 11 12 200