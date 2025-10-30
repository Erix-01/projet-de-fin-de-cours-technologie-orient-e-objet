
from abc import ABC, abstractmethod  # Pour gérer les classes abstraites en Python
import json
from typing import List, Dict, Any, Optional


# ===============================================================
# 1. CLASSE ABSTRAITE VEHICULE
# ---------------------------------------------------------------
# Rôle : Classe de base représentant tout véhicule louable.
# - Attributs communs : marque, modèle, année, prix journalier, disponibilité.
# - Méthodes abstraites : calculer_tarif_location() et afficher_details()
# ===============================================================
class Vehicule(ABC):
    def __init__(self, marque, modele, annee, prix_journalier, immatriculation: Optional[str] = None):
        self.__marque = marque
        self.__modele = modele
        self.__annee = annee
        self.__prix_journalier = prix_journalier
        self.__disponible = True  # Par défaut, un véhicule est disponible
        self.__immatriculation = immatriculation

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
        if etat in [True, False]:
            self.__disponible = etat
        else:
            raise ValueError("La disponibilité doit être True ou False.")
    
    def get_immatriculation(self):
        return self.__immatriculation

    def set_immatriculation(self, immat: str):
        self.__immatriculation = immat
        

    # --- Méthodes abstraites à implémenter dans les sous-classes ---
    @abstractmethod
    def calculer_tarif_location(self, nb_jours):
        pass

    @abstractmethod
    def afficher_details(self):
        pass

    # Sérialisation de base pour tous les véhicules
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.__class__.__name__,
            'marque': self.__marque,
            'modele': self.__modele,
            'annee': self.__annee,
            'prix_journalier': self.__prix_journalier,
            'disponible': self.__disponible,
            'immatriculation': self.__immatriculation,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        typ = data.get('type', 'Vehicule')
        if typ == 'Voiture':
            return Voiture.from_dict(data)
        if typ == 'Moto':
            return Moto.from_dict(data)
        # fallback to a generic Vehicule (not instantiable as abstract) -> create a simple Voiture
        return Voiture(data.get('marque'), data.get('modele'), data.get('annee'), data.get('prix_journalier'), nombre_portes=4)


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
              f"{self.get_nombre_portes()} portes - {self.get_prix_journalier()}fcfa/jour")

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({'nombre_portes': self.__nombre_portes})
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        v = cls(data.get('marque'), data.get('modele'), data.get('annee'), data.get('prix_journalier'), data.get('nombre_portes', 4))
        v.set_disponibilite(data.get('disponible', True))
        v.set_immatriculation(data.get('immatriculation'))
        return v


# ===============================================================
# 3. CLASSE MOTO (hérite de Vehicule)
# ---------------------------------------------------------------
# Rôle : Représente un véhicule de type moto.
# - Ajoute un attribut spécifique : cylindrée.
# - Redéfinit les méthodes abstraites.
# ===============================================================
class Moto(Vehicule):
    def __init__(self, marque, modele, annee, prix_journalier, cylindree: int = 500):
        super().__init__(marque, modele, annee, prix_journalier)
        self.__cylindree = cylindree


    def get_cylindree(self):
        return self.__cylindree

    def set_cylindree(self, c):
        self.__cylindree = c

    def calculer_tarif_location(self, nb_jours):
        total = self.get_prix_journalier() * nb_jours
        # Surtaxe de 15 % pour les grosses cylindrées
        if self.__cylindree > 600:
            total *= 1.15
        return total

    def afficher_details(self):
        print(f"Moto : {self.get_marque()} {self.get_modele()} ({self.get_annee()}) - "
              f"{self.get_cylindree()}cc - {self.get_prix_journalier()}fcfa/jour")

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({'cylindree': self.__cylindree})
        return base

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        m = cls(data.get('marque'), data.get('modele'), data.get('annee'), data.get('prix_journalier'), data.get('cylindree', 500))
        m.set_disponibilite(data.get('disponible', True))
        m.set_immatriculation(data.get('immatriculation'))
        return m


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
        return (f"{self.__prenom} {self.__nom} - Tél: {self.__telephone}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'nom': self.__nom,
            'prenom': self.__prenom,
            'telephone': self.__telephone
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(data.get('nom', ''), data.get('prenom', ''), data.get('telephone', ''))


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
        self.__mode_paiement = None  # Optionnel: mode de paiement utilisé

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
        print(f"Montant total : {self.__montant_total} fcfa")
        if self.__mode_paiement:
            print(f"Mode de paiement : {self.__mode_paiement}")
        print("===============================")

    def set_mode_paiement(self, mode):
        self.__mode_paiement = mode

    def get_mode_paiement(self):
        return self.__mode_paiement

    def to_dict(self) -> Dict[str, Any]:
        return {
            'client': self.__client.to_dict(),
            'vehicule': self.__vehicule.to_dict(),
            'nb_jours': self.__nb_jours,
            'montant_total': self.__montant_total,
            'mode_paiement': self.__mode_paiement.to_dict() if self.__mode_paiement else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        client = Client.from_dict(data.get('client', {}))
        vehicule = Vehicule.from_dict(data.get('vehicule', {}))
        nb_jours = data.get('nb_jours', 1)
        contrat = cls(client, vehicule, nb_jours)
        # montant_total recalculé dans __init__ ; si présent on peut l'assigner
        contrat.__montant_total = data.get('montant_total', contrat.get_montant_total())
        # mode de paiement
        mp = data.get('mode_paiement')
        if mp:
            contrat.set_mode_paiement(ModePaiement.from_dict(mp))
        return contrat






# ==============================
# Gestion des données
# ==============================
class GestionnaireDonnees:
    @staticmethod
    def sauvegarder(vehicules, clients, contrats):
        data = {
            "vehicules": [v.to_dict() for v in vehicules],
            "clients": [c.to_dict() for c in clients],
            "contrats": [c.to_dict() for c in contrats]
        }
        with open("donnees.json", "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("✅ Données sauvegardées dans donnees.json")

    @staticmethod
    def charger():
        try:
            with open("donnees.json", "r", encoding='utf-8') as f:
                data = json.load(f)
                print("✅ Données chargées avec succès")
                # reconstruire objets
                vehs = [Vehicule.from_dict(v) for v in data.get('vehicules', [])]
                clts = [Client.from_dict(c) for c in data.get('clients', [])]
                contrats = [ContratLocation.from_dict(c) for c in data.get('contrats', [])]
                return {"vehicules": vehs, "clients": clts, "contrats": contrats}
        except FileNotFoundError:
            print("⚠️ Aucune donnée trouvée. Nouveau départ.")
            return {"vehicules": [], "clients": [], "contrats": []}


# --------------------------------------------------
# Classe pour les modes de paiement
# --------------------------------------------------
class ModePaiement:
    """Représente un mode de paiement simple.

    Attributs : type ('carte' ou 'virement') et details (dict avec info pertinentes).
    """
    def __init__(self, type_mode: str, details: Optional[Dict[str, Any]] = None):
        self.type_mode = type_mode
        self.details = details or {}

    def __str__(self):
        return f"{self.type_mode} - {self.details}"

    def to_dict(self) -> Dict[str, Any]:
        return {'type_mode': self.type_mode, 'details': self.details}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(data.get('type_mode', 'unknown'), data.get('details', {}))

# Alias francophone pour compatibilité si utilisé ailleurs
ModePaiement = ModePaiement

