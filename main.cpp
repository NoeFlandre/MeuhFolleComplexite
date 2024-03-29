#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <unordered_map> // Ajout pour utiliser unordered_map

using namespace std;

// Structure afin de représenter un créneau
struct Creneau {
    string libelle;
    string plage_horaire;
    string type;
    int coefficient_priorite;
};

// Structure afin de représenter un bénévole
struct Benevole {
    string nom;
    unordered_map<string, int> score_coequipiers; // Nouveau: pour les scores des coéquipiers
    unordered_map<string, int> score_types_mission; // Pour les scores des types de mission
};

struct Equipe {
    string benevole1;
    string benevole2;
    int score = 0; // Pour tenir compte du score de l'équipe en fonction des préférences
};

// Fonction pour lire les données des créneaux à partir du fichier
vector<Creneau> lireCreneaux(const string& nom_fichier) {
    vector<Creneau> creneaux;
    ifstream fichier(nom_fichier);
    if (!fichier.is_open()) {
        cerr << "Erreur lors de l'ouverture du fichier " << nom_fichier << endl;
        return {}; // Retourne un vecteur vide en cas d'erreur
    }

    int nombre_creneaux;
    fichier >> nombre_creneaux;

    string ligne;
    getline(fichier, ligne); // Lire la ligne vide après le nombre de créneaux

    for (int i = 0; i < nombre_creneaux; ++i) {
        Creneau creneau;
        getline(fichier, creneau.libelle, ';');
        getline(fichier, creneau.plage_horaire, ';');
        getline(fichier, creneau.type, ';');
        fichier >> creneau.coefficient_priorite;
        getline(fichier, ligne); // Lire la fin de ligne pour passer à la prochaine entrée

        creneaux.push_back(creneau);
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
        return {}; // Retourne un vecteur vide en cas d'erreur
    }

    int nombre_benevoles;
    fichier >> nombre_benevoles;
    string ligne;
    getline(fichier, ligne); // Lire la ligne vide après le nombre de bénévoles

    for (int i = 0; i < nombre_benevoles; ++i) {
        Benevole benevole;
        getline(fichier, benevole.nom, ';');

        string choix1, choix2;
        getline(fichier, choix1, ';');
        getline(fichier, choix2, ';');
        if (!choix1.empty()) benevole.score_coequipiers[choix1] = 200; // Score pour le premier choix
        if (!choix2.empty()) benevole.score_coequipiers[choix2] = 100; // Score pour le second choix

        for (int j = 0; j < 3; ++j) {
            string choix;
            getline(fichier, choix, ';');
            if (!choix.empty()) {
                benevole.score_types_mission[choix] = 3 - j; // Attribue les scores 3, 2, 1
            }
        }

        benevoles.push_back(benevole);
        getline(fichier, ligne); // Lire la fin de ligne pour passer à la prochaine entrée
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

            auto it = benevole.score_types_mission.find(creneau.type);
            if (it != benevole.score_types_mission.end()) {
                int score_choix_coequipier = 0;
                auto itCo = benevole.score_coequipiers.find(creneau.libelle);
                if (itCo != benevole.score_coequipiers.end()) {
                    score_choix_coequipier = itCo->second;
                }

                int score_total = score_choix_coequipier + it->second;
                if (score_total > max_priorite) {
                    max_priorite = score_total;
                    index_benevole_max_priorite = i;
                }
            }
        }
    }

    return index_benevole_max_priorite;
}

int main() {
    vector<Creneau> creneaux = lireCreneaux("../Pb1.txt");
    vector<Benevole> benevoles = lireBenevoles("../Pb1.txt");

    vector<string> creneaux_affectes(benevoles.size(), "");
    vector<bool> benevole_utilise(benevoles.size(), false);

    for (auto& creneau : creneaux) {
        int index_benevole = trouverBenevoleMaxPriorite(benevoles, creneau, benevole_utilise);
        if (index_benevole != -1) {
            creneaux_affectes[index_benevole] = creneau.libelle;
            benevole_utilise[index_benevole] = true;
        }
    }

    cout << "Solution : " << endl;
    for (size_t i = 0; i < benevoles.size(); ++i) {
        cout << "Benevole : " << benevoles[i].nom << ", Creneau : " << creneaux_affectes[i] << endl;
    }

    return 0;
}
