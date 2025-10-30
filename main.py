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


from classes import *





# ==========================================================
# CLASSE SYSTÈME DE LOCATION
# ==========================================================
class SystemeLocation:
    def __init__(self):
        self.__vehicules = []
        self.__clients = []
        self.__contrats = []
        # Charger automatiquement les données si elles existent
        try:
            self.charger_donnees()
        except Exception:
            # en cas d'erreur de chargement, on continue avec des listes vides
            pass

    #getters pour les attributs privés
    def get_vehicule(self):
        return self.__vehicules
    
    def get_client(self):
        return self.__clients
    
    def get_contrat(self):
        return self.__contrats

    # --- Ajout de client ---
    def ajouter_client(self):
        nom = input("Nom du client : ")
        prenom = input("Prénom du client : ")
        telephone = input("Téléphone : ")
        client = Client(nom, prenom, telephone)
        self.__clients.append(client)
        print("✅ Client ajouté avec succès.\n")
        # sauvegarde immédiate
        try:
            self.sauvegarder_donnees()
        except Exception:
            pass

    # --- Affichage des clients ---
    def afficher_clients(self):
        if not self.__clients:
            print("Aucun client enregistré.")
        else:
            print("===== LISTE DES CLIENTS =====\n")
            for i, c in enumerate(self.__clients):
                print(f"{i + 1} - {c.afficher_details()}")
                
            print("=============================\n")

    # --- Ajout de véhicule ---
    def ajouter_vehicule(self):
        type_v = input("Type de véhicule (voiture/moto) : ")
        marque = input("Marque : ")
        modele = input("Modèle : ")
        annee = input("Année : ")
        immatriculation = input("Immatriculation : ")
        prix = float(input("Prix journalier : "))
        

        if type_v.lower() == "voiture":
            nombre_de_portes = int(input("Nombre de portes (pour voiture) : "))
            v = Voiture(marque, modele, annee, prix, nombre_de_portes, immatriculation=immatriculation)
        elif type_v.lower() == "moto":
            v = Moto(marque, modele, annee, prix_journalier=prix, immatriculation=immatriculation)
        else:
            return ("Type de véhicule invalide")
        
        

        self.__vehicules.append(v)
        print("✅ Véhicule ajouté avec succès.\n")
        try:
            self.sauvegarder_donnees()
        except Exception:
            pass

    # --- Affichage des véhicules ---
    def afficher_vehicules(self):   
        if not self.__vehicules:
            return ("Aucun véhicule enregistré.")
        
        print("\n===== LISTE DES VÉHICULES =====")
        for v in self.__vehicules:
            dispo = "Disponible" if v.est_disponible() else "Indisponible"
            print(f"- {v.get_marque()} {v.get_modele()} ({v.get_annee()}) immatriculation : {v.get_immatriculation()} | {dispo}")
        print("===============================\n")

    # --- Créer un contrat ---
    def creer_contrat(self):
        if not self.__clients or not self.__vehicules:
            print("⚠️ Vous devez d'abord ajouter des clients et des véhicules.")
            

        # Sélection du client
        print("\nListe des clients :")
        for i, c in enumerate(self.__clients):
            print(f"{i + 1}. {c.get_nom()}")
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
        try:
            self.sauvegarder_donnees()
        except Exception:
            pass

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

    # --- Persistence (sauvegarde / chargement) ---
    def sauvegarder_donnees(self):
        # utilise GestionnaireDonnees défini dans classes.py
        GestionnaireDonnees.sauvegarder(self.__vehicules, self.__clients, self.__contrats)

    def charger_donnees(self):
        data = GestionnaireDonnees.charger()
        # data contient des objets reconstruits
        self.__vehicules = data.get('vehicules', [])
        self.__clients = data.get('clients', [])
        self.__contrats = data.get('contrats', [])
    
    




# ==========================================================
# PROGRAMME PRINCIPAL
# ==========================================================
def main():
    systeme = SystemeLocation()
    
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Ajouter un client")
        print("2. Afficher la liste des clients")
        print("3. Ajouter un véhicule")
        print("4. Afficher la liste des véhicules")
        print("5. Créer un contrat de location")
        print("6. Afficher la liste des contrats actifs")
        print("7. Tester le polymorphisme (Voiture/Moto)")
        print("0. Quitter")

        choix = input("Votre choix : ")

        if choix == "1":
            systeme.ajouter_client()
        elif choix == "2":
            systeme.afficher_clients()
        elif choix == "3":
            systeme.ajouter_vehicule()
        elif choix == "4":
            systeme.afficher_vehicules()
        elif choix == "5":
            systeme.creer_contrat()
        elif choix == "6":
            systeme.afficher_contrats()
        elif choix == "7":
            systeme.tester_polymorphisme()
        elif choix == "0":
            print("👋 Au revoir !")
            break
        else:
            return("Choix invalide, veuillez réessayer.")
        
        

        






if __name__ == "__main__":
    main()





