
from abc import ABC, abstractmethod  # Pour gérer les classes abstraites en Python


# ===============================================================
# 1. CLASSE ABSTRAITE VEHICULE
# ---------------------------------------------------------------
# Rôle : Classe de base représentant tout véhicule louable.
# - Attributs communs : marque, modèle, année, prix journalier, disponibilité.
# - Méthodes abstraites : calculer_tarif_location() et afficher_details()
# ===============================================================
class Vehicule(ABC):
    def __init__(self, marque, modele, annee, prix_journalier):
        self.__marque = marque
        self.__modele = modele
        self.__annee = annee
        self.__prix_journalier = prix_journalier
        self.__disponible = True  # Par défaut, un véhicule est disponible

    # --- Getters et Setters (Encapsulation) ---
    def get_marque(self):
        return self.__marque

    def set_marque(self, marque):
        self.__marque = marque

    def get_modele(self):
        return self.__modele

    def set_modele(self, modele):
        self.__modele = modele

    def get_annee(self):
        return self.__annee

    def set_annee(self, annee):
        self.__annee = annee

    def get_prix_journalier(self):
        return self.__prix_journalier

    def set_prix_journalier(self, prix):
        self.__prix_journalier = prix

    def est_disponible(self):
        return self.__disponible

    def set_disponibilite(self, etat):
        self.__disponible = etat

    # --- Méthodes abstraites à implémenter dans les sous-classes ---
    @abstractmethod
    def calculer_tarif_location(self, nb_jours):
        pass

    @abstractmethod
    def afficher_details(self):
        pass


    # ===============================================================
# 2. CLASSE VOITURE (hérite de Vehicule)
# ---------------------------------------------------------------
# Rôle : Représente un véhicule de type voiture.
# - Ajoute un attribut spécifique : nombre de portes.
# - Redéfinit les méthodes abstraites de Vehicule.
# ===============================================================
class Voiture(Vehicule):
    def __init__(self, marque, modele, annee, prix_journalier, nombre_portes):
        super().__init__(marque, modele, annee, prix_journalier)
        self.__nombre_portes = nombre_portes

    def get_nombre_portes(self):
        return self.__nombre_portes

    def set_nombre_portes(self, nb):
        self.__nombre_portes = nb

    # Redéfinition de la méthode de calcul du tarif (Polymorphisme)
    def calculer_tarif_location(self, nb_jours):
        total = self.get_prix_journalier() * nb_jours
        # Réduction de 10 % si la location dépasse 7 jours
        if nb_jours > 7:
            total *= 0.9
        return total

    # Redéfinition de l’affichage des détails
    def afficher_details(self):
        print(f"Voiture : {self.get_marque()} {self.get_modele()} ({self.get_annee()}) - "
              f"{self.get_nombre_portes()} portes - {self.get_prix_journalier()}€/jour")


# ===============================================================
# 3. CLASSE MOTO (hérite de Vehicule)
# ---------------------------------------------------------------
# Rôle : Représente un véhicule de type moto.
# - Ajoute un attribut spécifique : cylindrée.
# - Redéfinit les méthodes abstraites.
# ===============================================================
class Moto(Vehicule):
    def __init__(self, marque, modele, annee, prix_journalier, cylindree):
        super().__init__(marque, modele, annee, prix_journalier)
        self.__cylindree = cylindree

    def get_cylindree(self):
        return self.__cylindree

    def set_cylindree(self, cylindree):
        self.__cylindree = cylindree

    def calculer_tarif_location(self, nb_jours):
        total = self.get_prix_journalier() * nb_jours
        # Surtaxe de 15 % pour les grosses cylindrées
        if self.__cylindree > 600:
            total *= 1.15
        return total

    def afficher_details(self):
        print(f"Moto : {self.get_marque()} {self.get_modele()} ({self.get_annee()}) - "
              f"{self.get_cylindree()}cc - {self.get_prix_journalier()}€/jour")


# ===============================================================
# 4. CLASSE CLIENT
# ---------------------------------------------------------------
# Rôle : Représente un client de l’entreprise.
# - Un client peut avoir plusieurs contrats de location.
# - Stocke les informations personnelles.
# ===============================================================
class Client:
    def __init__(self, nom, prenom, telephone):
        self.__nom = nom
        self.__prenom = prenom
        self.__telephone = telephone

    def get_nom(self):
        return self.__nom

    def set_nom(self, nom):
        self.__nom = nom

    def get_prenom(self):
        return self.__prenom

    def set_prenom(self, prenom):
        self.__prenom = prenom

    def get_telephone(self):
        return self.__telephone

    def set_telephone(self, telephone):
        self.__telephone = telephone

    def afficher_details(self):
        print(f"Client : {self.__prenom} {self.__nom} - Tél: {self.__telephone}")


# ===============================================================
# 5. CLASSE CONTRATLOCATION
# ---------------------------------------------------------------
# Rôle : Associe un client à un véhicule pour une durée donnée.
# - Calcule le montant total de la location.
# - Rend le véhicule indisponible pendant la période.
# ===============================================================
class ContratLocation:
    def __init__(self, client, vehicule, nb_jours):
        self.__client = client
        self.__vehicule = vehicule
        self.__nb_jours = nb_jours
        self.__montant_total = vehicule.calculer_tarif_location(nb_jours)
        vehicule.set_disponibilite(False)  # Le véhicule n’est plus disponible

    def get_client(self):
        return self.__client

    def get_vehicule(self):
        return self.__vehicule

    def get_nb_jours(self):
        return self.__nb_jours

    def get_montant_total(self):
        return self.__montant_total

    def afficher_details(self):
        print("===== Contrat de location =====")
        self.__client.afficher_details()
        self.__vehicule.afficher_details()
        print(f"Durée : {self.__nb_jours} jours")
        print(f"Montant total : {self.__montant_total} €")
        print("===============================")






# ==============================
# Gestion des données
# ==============================
class GestionnaireDonnees:
    @staticmethod
    def sauvegarder(vehicules, clients, contrats):
        data = {
            "vehicules": [v.get_immatriculation() for v in vehicules],
            "clients": [c.get_nom_complet() for c in clients],
            "contrats": [vars(c) for c in contrats]
        }
        with open("donnees.json", "w") as f:
            json.dump(data, f, indent=4)
        print("✅ Données sauvegardées dans donnees.json")

    @staticmethod
    def charger():
        try:
            with open("donnees.json", "r") as f:
                data = json.load(f)
                print("✅ Données chargées avec succès")
                return data
        except FileNotFoundError:
            print("⚠️ Aucune donnée trouvée. Nouveau départ.")
            return {"vehicules": [], "clients": [], "contrats": []}

