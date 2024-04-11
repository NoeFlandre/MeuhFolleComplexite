import time

# Définition de la classe Creneau, qui modélise un créneau disponible pour l'affectation des bénévoles.
class Creneau:
    def __init__(self, label, plage_horaire, type_mission, coefficient):
        # Identifiant unique du créneau.
        self.label = label
        # Plage horaire du créneau.
        self.plage_horaire = plage_horaire
        # Type de mission associée au créneau (ex : Bar, Camping).
        self.type_mission = type_mission
        # Coefficient de priorité du créneau, indiquant son importance.
        self.coefficient = coefficient

    def __repr__(self):
        # Représentation textuelle d'un créneau pour faciliter le débogage.
        return f"Creneau(Label: {self.label}, Horaire: {self.plage_horaire}, Type: {self.type_mission}, Coeff: {self.coefficient})"

# Définition de la classe Benevole, qui représente un bénévole participant au festival.
class Benevole:
    def __init__(self, nom, choix_coquipiers, choix_missions):
        self.nom = nom  # Nom du bénévole.
        # Préférences de coéquipiers, stockées sous forme de dictionnaire pour un accès rapide.
        self.choix_coquipiers = {nom: coeff for nom, coeff in choix_coquipiers}
        # Préférences de type de missions, également stockées sous forme de dictionnaire.
        self.choix_missions = {type_mission: coeff for type_mission, coeff in choix_missions}
        self.affecte = False  # Indique si le bénévole a déjà été affecté à un créneau.

# Fonction pour lire les données des bénévoles et des créneaux à partir d'un fichier texte.
def lire_fichier(fichier):
    creneaux = []  # Liste pour stocker les créneaux disponibles.
    benevoles = {}  # Dictionnaire pour stocker les informations des bénévoles.
    
    with open(fichier, "r") as f:
        n_line = f.readline().strip()  # Lecture du nombre de créneaux.
        n = int(n_line.split()[0])
        
        # Lecture et stockage des créneaux.
        for _ in range(n):
            parts = f.readline().strip().split(";")
            creneaux.append(Creneau(parts[0], parts[1], parts[2], int(parts[3])))
        
        m_line = f.readline().strip()  # Lecture du nombre de bénévoles.
        m = int(m_line.split()[0])
        
        # Lecture et stockage des informations des bénévoles.
        for _ in range(m):
            parts = f.readline().strip().split(";")
            nom = parts[0]
            choix_coquipiers = [(parts[i], int(200 if i == 4 else 100)) for i in range(4, 6) if parts[i] != 'nochoice']
            choix_missions = [(parts[i], int(3-i+1)) for i in range(1, 4) if parts[i] != 'nochoice']
            benevoles[nom] = Benevole(nom, choix_coquipiers, choix_missions)
    
    return creneaux, benevoles

# Fonction pour optimiser les affectations des bénévoles aux créneaux disponibles.
def optimiser_affectations(creneaux, benevoles):
    affectations = []  # Liste pour stocker les affectations optimales.
    valeur_objectif = 0  # Valeur initiale de la fonction objectif.

    # Trier les créneaux par ordre décroissant de coefficient pour prioriser les plus importants.
    creneaux.sort(key=lambda x: -x.coefficient)

    # Boucle pour former des binômes de bénévoles pour chaque créneau.
    for creneau in creneaux:
        meilleur_score = -float('inf')
        meilleure_combinaison = None

        # Double boucle pour comparer chaque paire de bénévoles non affectés.
        for nom1, ben1 in benevoles.items():
            for nom2, ben2 in benevoles.items():
                if nom1 != nom2 and not ben1.affecte and not ben2.affecte:
                    score = creneau.coefficient
                    # Calcul du score basé sur les préférences de missions et de coéquipiers.
                    score += ben1.choix_missions.get(creneau.type_mission, 0) + ben2.choix_missions.get(creneau.type_mission, 0)
                    score += ben1.choix_coquipiers.get(nom2, 0) + ben2.choix_coquipiers.get(nom1, 0)

                    if score > meilleur_score:
                        meilleur_score = score
                        meilleure_combinaison = (nom1, nom2)

        # Affectation du binôme au créneau si une combinaison optimale a été trouvée.
        if meilleure_combinaison:
            benevoles[meilleure_combinaison[0]].affecte = True
            benevoles[meilleure_combinaison[1]].affecte = True
            affectations.append((creneau.label, meilleure_combinaison[0], meilleure_combinaison[1]))
            valeur_objectif += meilleur_score

    return affectations, valeur_objectif

# Point d'entrée principal pour exécuter le programme.

if __name__ == "__main__":
    chemin_fichier = "Pb8.txt"

    # Démarrage du chronomètre juste avant de commencer l'optimisation
    start_time = time.time()

    # Lecture des données et optimisation des affectations
    creneaux, benevoles = lire_fichier(chemin_fichier)
    affectations, valeur_objectif = optimiser_affectations(creneaux, benevoles)

    # Arrêt du chronomètre après l'optimisation
    end_time = time.time()

    # Calcul du temps CPU en secondes
    cpu_time = end_time - start_time

    print("Affectations optimales :")
    for affectation in affectations:
        creneau_label, benevole_1, benevole_2 = affectation
        # Trouver le créneau correspondant au label pour obtenir le type de mission.
        creneau = next((c for c in creneaux if c.label == creneau_label), None)
        type_mission = creneau.type_mission if creneau else "Inconnu"
        print(f"{creneau_label};{type_mission};{benevole_1};{benevole_2}")
    print(f"\nValeur de l'objectif : {valeur_objectif}")
    print(f"Temps CPU : {cpu_time:.2f} secondes")  # Affiche le temps CPU avec 2 décimales


