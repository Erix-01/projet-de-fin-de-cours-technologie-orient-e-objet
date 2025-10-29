 # ===============================================================
# PROJET DE FIN DE COURS
# Système de Gestion d’Entreprise de Location de Véhicules
# ===============================================================
# Étape 1 & 2 :
# Objectif :
# - Mettre en pratique les concepts fondamentaux de la POO :
#   Classes, Objets, Encapsulation, Héritage, Polymorphisme, Abstraction.
# - Organiser les relations logiques entre les classes sans UML formel.
# ---------------------------------------------------------------
# Ce code illustre la modélisation de base du système ACA :
#  - Gestion des véhicules (voitures et motos)
#  - Gestion des clients
#  - Gestion des contrats de location
# ---------------------------------------------------------------

from abc import ABC, abstractmethod  # Pour gérer les classes abstraites en Python
from classes import *




# ==========================================================
# CLASSE SYSTÈME DE LOCATION
# ==========================================================
class SystemeLocation:
    def __init__(self):
        self.__vehicules = []
        self.__clients = []
        self.__contrats = []

    # --- Ajout de client ---
    def ajouter_client(self):
        nom = input("Nom du client : ")
        prenom = input("Prénom du client : ")
        telephone = input("Téléphone : ")
        client = Client(nom, prenom, telephone)
        self.__clients.append(client)
        print("✅ Client ajouté avec succès.\n")

    # --- Ajout de véhicule ---
    def ajouter_vehicule(self):
        type_v = input("Type de véhicule (voiture/moto) : ").lower()
        marque = input("Marque : ")
        modele = input("Modèle : ")
        annee = input("Année : ")

        if type_v == "voiture":
            v = Voiture(marque, modele, annee)
        elif type_v == "moto":
            v = Moto(marque, modele, annee)
        else:
            print("Type de véhicule invalide.")
            return

        self.__vehicules.append(v)
        print("✅ Véhicule ajouté avec succès.\n")

    # --- Créer un contrat ---
    def creer_contrat(self):
        if not self.__clients or not self.__vehicules:
            print("⚠️ Vous devez d'abord ajouter des clients et des véhicules.")
            

        # Sélection du client
        print("\nListe des clients :")
        for i, c in enumerate(self.__clients):
            print(f"{i + 1}. {c.get_nom_complet()}")
        choix_client = int(input("Choisissez un client : ")) - 1
        client = self.__clients[choix_client]

        # Sélection du véhicule disponible
        print("\nVéhicules disponibles :")
        disponibles = [v for v in self.__vehicules if v.est_disponible()]
        if not disponibles:
            print("Aucun véhicule disponible.")
            

        for i, v in enumerate(disponibles):
            print(f"{i + 1}. {v.get_marque()} {v.get_modele()}")
        choix_vehicule = int(input("Choisissez un véhicule : ")) - 1
        vehicule = disponibles[choix_vehicule]

        # Durée de location
        nb_jours = int(input("Nombre de jours de location : "))

        # Création du contrat
        contrat = ContratLocation(client, vehicule, nb_jours)
        self.__contrats.append(contrat)
        print("\n✅ Contrat créé avec succès !\n")
        contrat.afficher_details()

    # --- Afficher tous les contrats actifs ---
    def afficher_contrats(self):
        if not self.__contrats:
            print("Aucun contrat enregistré.")
            return
        print("\n===== LISTE DES CONTRATS ACTIFS =====")
        for c in self.__contrats:
            c.afficher_details()

    # --- Test polymorphisme ---
    def tester_polymorphisme(self):
        print("\n=== TEST DU POLYMORPHISME ===")
        for v in self.__vehicules:
            v.afficher_details()



# ==========================================================
# PROGRAMME PRINCIPAL
# ==========================================================
def main():
    systeme = SystemeLocation()

    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Ajouter un client")
        print("2. Ajouter un véhicule")
        print("3. Créer un contrat de location")
        print("4. Afficher la liste des contrats actifs")
        print("5. Tester le polymorphisme (Voiture/Moto)")
        print("0. Quitter")

        choix = input("Votre choix : ")

        if choix == "1":
            systeme.ajouter_client()
        elif choix == "2":
            systeme.ajouter_vehicule()
        elif choix == "3":
            systeme.creer_contrat()
        elif choix == "4":
            systeme.afficher_contrats()
        elif choix == "5":
            systeme.tester_polymorphisme()
        elif choix == "0":
            print("👋 Au revoir !")
            break
        else:
            print("Choix invalide, veuillez réessayer.")






if __name__ == "__main__":
    main()





