#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>

using namespace std;

// Structure afin de représenter un créneau
struct Creneau {
    string libelle;
    string plage_horaire;
    string type;
    int coefficient_priorite;
};

// Structure pour représenter un bénévole
struct Benevole {
    string nom;
    vector<string> choix_coequipiers;
    vector<string> choix_types_mission;
};

// Fonction pour lire les données des créneaux à partir du fichier
vector<Creneau> lireCreneaux(const string& nom_fichier) {
    vector<Creneau> creneaux;
    ifstream fichier(nom_fichier);
    if (!fichier.is_open()) {
        cerr << "Erreur lors de l'ouverture du fichier " << nom_fichier << endl;
        return creneaux;
    }

    int nombre_creneaux;
    fichier >> nombre_creneaux; // Lire le nombre de créneaux

    string ligne;
    getline(fichier, ligne); // Lire la ligne vide après le nombre de créneaux

    for (int i = 0; i < nombre_creneaux; ++i) {
        Creneau creneau;
        getline(fichier, creneau.libelle, ';');
        getline(fichier, creneau.plage_horaire, ';');
        getline(fichier, creneau.type, ';');
        fichier >> creneau.coefficient_priorite;

        creneaux.push_back(creneau);
        getline(fichier, ligne); // Lire la fin de ligne
    }

    fichier.close();
    return creneaux;
}

// Fonction pour lire les données des bénévoles à partir du fichier
vector<Benevole> lireBenevoles(const string& nom_fichier) {
    vector<Benevole> benevoles;
    ifstream fichier(nom_fichier);
    if (!fichier.is_open()) {
        cerr << "Erreur lors de l'ouverture du fichier " << nom_fichier << endl;
        return benevoles;
    }

    int nombre_benevoles;
    fichier >> nombre_benevoles; // Lire le nombre de bénévoles

    string ligne;
    getline(fichier, ligne); // Lire la ligne vide après le nombre de bénévoles

    for (int i = 0; i < nombre_benevoles; ++i) {
        Benevole benevole;
        getline(fichier, benevole.nom, ';');

        for (int j = 0; j < 2; ++j) {
            string choix;
            getline(fichier, choix, ';');
            if (!choix.empty()) {
                benevole.choix_coequipiers.push_back(choix);
            }
        }

        for (int j = 0; j < 3; ++j) {
            string choix;
            getline(fichier, choix, ';');
            if (!choix.empty()) {
                benevole.choix_types_mission.push_back(choix);
            }
        }

        benevoles.push_back(benevole);
        getline(fichier, ligne); // Lire la fin de ligne
    }

    fichier.close();
    return benevoles;
}

// Fonction pour trouver le bénévole avec le coefficient de priorité le plus élevé pour un créneau donné
int trouverBenevoleMaxPriorite(const vector<Benevole>& benevoles, const Creneau& creneau, vector<bool>& benevole_utilise) {
    int max_priorite = -1;
    int index_benevole_max_priorite = -1;

    for (size_t i = 0; i < benevoles.size(); ++i) {
        if (!benevole_utilise[i]) {
            const auto& benevole = benevoles[i];
            for (const auto& choix : benevole.choix_types_mission) {
                if (choix == creneau.type) {
                    int priorite = benevole.choix_coequipiers[0] == creneau.libelle ? 200 : (benevole.choix_coequipiers[1] == creneau.libelle ? 100 : 0);
                    if (priorite > max_priorite) {
                        max_priorite = priorite;
                        index_benevole_max_priorite = i;
                    }
                }
            }
        }
    }

    return index_benevole_max_priorite;
}

int main() {
    // Lecture des créneaux depuis le fichier Pb0.txt
    vector<Creneau> creneaux = lireCreneaux("../Pb1.txt");

    // Lecture des bénévoles depuis le fichier Pb0.txt
    vector<Benevole> benevoles = lireBenevoles("../Pb1.txt");

    // Vecteur pour stocker les créneaux affectés à chaque bénévole
    vector<string> creneaux_affectes(benevoles.size(), "");

    // Vecteur pour marquer les bénévoles déjà affectés à un créneau
    vector<bool> benevole_utilise(benevoles.size(), false);

    // Affectation des créneaux aux bénévoles
    for (auto& creneau : creneaux) {
        int index_benevole = trouverBenevoleMaxPriorite(benevoles, creneau, benevole_utilise);
        if (index_benevole != -1) {
            creneaux_affectes[index_benevole] = creneau.libelle;
            benevole_utilise[index_benevole] = true;
        }
    }

    // Affichage de la solution
    cout << "Solution : " << endl;
    for (size_t i = 0; i < benevoles.size(); ++i) {
        cout << "Benevole : " << benevoles[i].nom << ", Creneau : " << creneaux_affectes[i] << endl;
    }

    return 0;
}
