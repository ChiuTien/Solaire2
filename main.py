from Models.Consommation import Consommation
from Services.PanneauService import PanneauService
from Services.ConsommationService import ConsommationService

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

#nouvelle_liste = PanneauService.calculer_consommation_fusionnee(consommations)

#for c in nouvelle_liste:
#    print(c.get_heureDebut(), c.get_heureFin(), c.get_consommation())
# 6 7 500
# 7 9 800
# 9 10 500
# 11 12 200


def as_tuple(conso):
    return (
        conso.get_idAppareil(),
        conso.get_heureDebut(),
        conso.get_heureFin(),
        conso.get_consommation(),
    )


# Test ajoute avec tes donnees pour la separation journee/soiree.
consommation_journee = ConsommationService.retourner_consommation_journee(consommations)
consommation_soiree = ConsommationService.retourner_consommation_soiree(consommations)



#consommation_journee = PanneauService.calculer_consommation_fusionnee(consommation_journee)
print("Consommation journee:")
for c in consommation_journee:
    print(as_tuple(c))
print("Consommation soiree:")
for c in consommation_soiree:
    print(as_tuple(c))
pic = PanneauService.retourner_pic(consommation_journee)
if pic:
    print(pic.get_heureDebut(), pic.get_heureFin(), pic.get_consommation())


print("Tests ConsommationService OK")