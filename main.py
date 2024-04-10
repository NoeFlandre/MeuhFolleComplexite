class Creneau:
    def __init__(self, label, plage_horaire, type_mission, coefficient):
        self.label = label
        self.plage_horaire = plage_horaire
        self.type_mission = type_mission
        self.coefficient = coefficient

class Benevole:
    def __init__(self, nom, choix_coquipiers, choix_missions):
        self.nom = nom
        # Transformation des préférences de coéquipiers en dictionnaire pour un accès rapide
        self.choix_coquipiers = {nom: coeff for nom, coeff in choix_coquipiers}
        # Transformation des préférences de missions en dictionnaire pour un accès rapide
        self.choix_missions = {type_mission: coeff for type_mission, coeff in choix_missions}
        self.affecte = False  # Pour suivre si le bénévole a été affecté

def lire_fichier(fichier):
    creneaux = []
    benevoles = {}
    
    with open(fichier, "r") as f:
        n_line = f.readline().strip()
        n = int(n_line.split()[0])
        
        for _ in range(n):
            parts = f.readline().strip().split(";")
            creneaux.append(Creneau(parts[0], parts[1], parts[2], int(parts[3])))
        
        m_line = f.readline().strip()
        m = int(m_line.split()[0])
        
        for _ in range(m):
            parts = f.readline().strip().split(";")
            nom = parts[0]
            choix_coquipiers = [(parts[i], int(200 if i == 4 else 100)) for i in range(4, 6) if parts[i] != 'nochoice']
            choix_missions = [(parts[i], int(3-i+1)) for i in range(1, 4) if parts[i] != 'nochoice']
            benevoles[nom] = Benevole(nom, choix_coquipiers, choix_missions)
    
    return creneaux, benevoles

def optimiser_affectations(creneaux, benevoles):
    # Initialisation
    affectations = []
    valeur_objectif = 0

    # Trier les créneaux par ordre décroissant de coefficient pour prioriser les plus importants
    creneaux.sort(key=lambda x: -x.coefficient)

    # Former des binômes
    for creneau in creneaux:
        meilleur_score = -float('inf')
        meilleure_combinaison = None

        # Parcourir tous les bénévoles pour trouver le meilleur binôme pour chaque créneau
        for nom1, ben1 in benevoles.items():
            for nom2, ben2 in benevoles.items():
                if nom1 != nom2 and not ben1.affecte and not ben2.affecte:
                    score = creneau.coefficient
                    # Ajouter les scores basés sur les préférences des missions
                    score += ben1.choix_missions.get(creneau.type_mission, 0) + ben2.choix_missions.get(creneau.type_mission, 0)
                    # Ajouter les scores basés sur les préférences de coéquipiers
                    score += ben1.choix_coquipiers.get(nom2, 0) + ben2.choix_coquipiers.get(nom1, 0)

                    if score > meilleur_score:
                        meilleur_score = score
                        meilleure_combinaison = (nom1, nom2)

        if meilleure_combinaison:
            benevoles[meilleure_combinaison[0]].affecte = True
            benevoles[meilleure_combinaison[1]].affecte = True
            affectations.append((creneau.label, meilleure_combinaison[0], meilleure_combinaison[1]))
            valeur_objectif += meilleur_score

    return affectations, valeur_objectif

if __name__ == "__main__":
    chemin_fichier = "Pb0.txt"
    creneaux, benevoles = lire_fichier(chemin_fichier)
    affectations, valeur_objectif = optimiser_affectations(creneaux, benevoles)

    print("Affectations optimales :")
    for affectation in affectations:
        print(f"{affectation[0]} attribué à {affectation[1]} et {affectation[2]}")
    print(f"\nValeur de l'objectif : {valeur_objectif}")
