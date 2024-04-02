# Cette classe représente un créneau avec ses caractéristiques.
class Creneau:
    def __init__(self, label, plage_horaire, type_mission, coefficient):
        self.label = label
        self.plage_horaire = plage_horaire
        self.type_mission = type_mission
        self.coefficient = coefficient

    def __repr__(self):
        return f"\nCreneau(Label: {self.label}, Horaire: {self.plage_horaire}, Type: {self.type_mission}, Coeff: {self.coefficient})\n"

# Cette classe représente un bénévole avec ses choix de coéquipiers et missions.
class Benevole:
    def __init__(self, nom, choix_coquipiers, choix_missions):
        self.nom = nom
        self.choix_coquipiers = choix_coquipiers  # [(coequipier, coeff), ...]
        self.choix_missions = choix_missions  # [(type_mission, coeff), ...]

    def __repr__(self):
        return f"\nBenevole(Nom: {self.nom}, Coequipiers: {self.choix_coquipiers}, Missions: {self.choix_missions})\n"

# Cette fonction lit le contenu d'un fichier et crée les objets Creneau et Benevole correspondants.
def lire_fichier(fichier):
    creneaux = []
    benevoles = []
    
    with open(fichier, "r") as f:
        n_line = f.readline().strip()
        n = int(n_line.split()[0])
        
        # Lire les informations sur les créneaux
        for _ in range(n):
            label, plage_horaire, type_mission, coeff = f.readline().strip().split(";")
            creneaux.append(Creneau(label, plage_horaire, type_mission, int(coeff)))
        
        m_line = f.readline().strip()
        m = int(m_line.split()[0])
        
        # Lire les informations sur les bénévoles
        for _ in range(m):
            data = f.readline().strip().split(";")
            nom = data[0]
            choix_coquipiers = [(data[4], 200), (data[5], 100) if data[5] != 'nochoice' else (None, 0)]
            choix_missions = [(data[1], 3), (data[2], 2) if data[2] != 'nochoice' else (None, 0), (data[3], 1) if data[3] != 'nochoice' else (None, 0)]
            benevoles.append(Benevole(nom, choix_coquipiers, choix_missions))
    
    return creneaux, benevoles

# Cette fonction trouve la solution optimale en affectant les bénévoles aux créneaux.
def trouver_solution_optimale(creneaux, benevoles):
    # Étape 1: Créer les paires de bénévoles en fonction de leurs préférences et coefficients
    paires_benevoles = creer_paires(benevoles)  # Cette fonction reste à implémenter
    
    # Étape 2: Affecter les paires aux créneaux en maximisant les coefficients
    affectations = affecter_creneaux(paires_benevoles, creneaux)  # Cette fonction reste à implémenter
    
    return affectations

# Cette fonction crée des paires de bénévoles en fonction de leurs préférences et coefficients.

def creer_paires(benevoles):
    paires = []
    apparies = set()
    
    # Convertir la liste des bénévoles en un dictionnaire pour un accès facile par le nom
    benevoles_dict = {benevole.nom: benevole for benevole in benevoles}

    for benevole in benevoles:
        if benevole.nom not in apparies:
            for choix, coeff in benevole.choix_coquipiers:
                if choix in benevoles_dict and choix not in apparies:
                    # Ajouter la paire d'objets Benevole
                    paires.append((benevole, benevoles_dict[choix]))
                    apparies.add(benevole.nom)
                    apparies.add(choix)
                    break  # Sortir dès qu'une paire est formée

    return paires


# Cette fonction affecte les paires de bénévoles aux créneaux en maximisant les coefficients.
def affecter_creneaux(paires, creneaux):
    affectations = []
    creneaux.sort(key=lambda x: x.coefficient, reverse=True)

    # Suivre les créneaux déjà affectés pour éviter les duplications
    creneaux_affectes = set()

    # D'abord, essayer d'affecter les paires aux créneaux selon les préférences
    for creneau in creneaux:
        meilleure_paire = None
        meilleur_score = -1

        for paire in paires:
            benevole1, benevole2 = paire
            score = sum(pref[1] for pref in benevole1.choix_missions if pref[0] == creneau.type_mission) + \
                    sum(pref[1] for pref in benevole2.choix_missions if pref[0] == creneau.type_mission)

            # Vérifier si cette paire est la meilleure trouvée et si le créneau n'a pas encore été affecté
            if score > meilleur_score and creneau not in creneaux_affectes:
                meilleur_score = score
                meilleure_paire = paire

        if meilleure_paire:
            affectations.append((creneau, meilleure_paire))
            creneaux_affectes.add(creneau)
            paires.remove(meilleure_paire)  # Retirer la paire affectée de la liste des paires disponibles

    # Si des bénévoles n'ont pas été affectés après la première répartition
    if len(paires) > 0:
        # Affecter les paires restantes aux créneaux restants
        for creneau in creneaux:
            if creneau not in creneaux_affectes and paires:
                meilleure_paire = paires.pop(0)  # Prendre la prochaine paire disponible
                affectations.append((creneau, meilleure_paire))
                creneaux_affectes.add(creneau)

    return affectations





# Exemple d'utilisation (à exécuter dans votre environnement local)
chemin_fichier = "Pb0.txt"
creneaux, benevoles = lire_fichier(chemin_fichier)
paires = creer_paires(benevoles)
#print(paires)
#print(affecter_creneaux(paires, creneaux))
#print(creneaux)
#print(benevoles)
print(trouver_solution_optimale(creneaux, benevoles))

# Ce code a été ajusté pour corriger l'ordre des paramètres dans la création des objets Benevole
# et pour traiter correctement les lignes d'introduction des sections créneaux et bénévoles.
