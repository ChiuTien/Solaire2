from Models.Consommation import Consommation
from Models.EnergieSolaire import EnergieSolaire
from Services.PanneauService import PanneauService
from Services.ConsommationService import ConsommationService

consommations = [
    Consommation(None, 1, "8h", "12h", 55),#TV
    Consommation(None, 1, "10", "14", 75),#Ventillateur
    Consommation(None, 1, "6", "17", 120),#Refrigerateur
    Consommation(None, 1, "17", "19", 10),#lampe
    Consommation(None, 1, "17", "19", 55),#tv
    Consommation(None, 1, "19", "6", 10),#routeur wifi
    Consommation(None, 1, "19", "6", 120),#refrigerateur
    Consommation(None, 1, "19", "23", 10)#lampe
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



print("Consommation journee:")
for c in consommation_journee:
    print(as_tuple(c))
    
consommation_journee = PanneauService.calculer_consommation_fusionnee(consommation_journee)
    
print("Consommation journee:")
for c in consommation_journee:
    print(as_tuple(c))
print("Consommation soiree:")
for c in consommation_soiree:
    print(as_tuple(c))
pic = PanneauService.retourner_pic(consommation_journee)
if pic:
    print(pic.get_heureDebut(), pic.get_heureFin(), pic.get_consommation())

energie_solaires = [
    EnergieSolaire(None, "AM", 1, "6", "17", None),
    EnergieSolaire(None, "FA", 0.5, "17", "19", None),
    EnergieSolaire(None, "PM", 0, "19", "6", None),
]

puissance_scolaire = PanneauService.calcul_puissance_scolaire(consommation_journee, energie_solaires)
puissance_restante = PanneauService.calcul_puissance_restante(consommation_journee, energie_solaires)

print("Puissance scolaire:", puissance_scolaire)
print("Puissance restante:", puissance_restante)


print("Tests ConsommationService OK")