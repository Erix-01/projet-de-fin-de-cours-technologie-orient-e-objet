# Projet de fin de cours - Système de gestion de location

Ce document explique, de façon simple, les étapes de création du projet et comment utiliser le programme
pour gérer des clients, des véhicules et des contrats (avec persistance JSON).

## 1) Contenu du dépôt

- `classes.py` : définitions des classes principales (Vehicule, Voiture, Moto, Client, ContratLocation),
	gestion de la sérialisation (to_dict / from_dict) et `GestionnaireDonnees` pour lire/écrire `donnees.json`.
- `main.py` : interface console simple pour ajouter/afficher clients et véhicules, créer des contrats et
	sauvegarder/charger automatiquement les données.
- `donnees.json` : fichier généré automatiquement qui contient les clients, véhicules et contrats sauvegardés.

## 2) Prérequis

- Python 3.7+ installé.
- Aucun paquet externe nécessaire (utilise uniquement la bibliothèque standard).

## 3) Comment lancer

Ouvrir un terminal (PowerShell sous Windows) et exécuter :

```powershell
python "c:\Users\HP\Desktop\tp too\projet de fin de cours\main.py"
```

Le programme ouvre un menu interactif. Suivre les options pour ajouter des clients, véhicules et créer des contrats.

## 4) Flux d'utilisation (étapes simples)

1. Ajouter un client (menu option 1) : renseigner nom, prénom, téléphone.
2. Ajouter un véhicule (menu option 3) : choisir type (`voiture` ou `moto`) puis renseigner marque, modèle, année et prix.
3. Créer un contrat (menu option 5) : sélectionner un client, choisir un véhicule disponible et indiquer le nombre de jours.
	 - Lors de la création du contrat, le véhicule est marqué comme indisponible.
4. Quitter le programme (option 0) : les modifications sont sauvegardées dans `donnees.json` automatiquement.

Remarque : le programme sauvegarde automatiquement après chaque ajout/modification (ajout client, véhicule, création de contrat).

## 5) Persistance des données

- `GestionnaireDonnees` écrit un fichier `donnees.json` contenant des objets sérialisés (dicts).
- Au démarrage, `SystemeLocation` tente de charger `donnees.json` et reconstruit les objets (clients, véhicules, contrats).

## 6) Modes de paiement

- Le projet contient une classe `ModePaiement` simple qui permet de stocker le type (`carte` ou `virement`) et des
	détails (ex : numéro de carte masqué, IBAN partiel). Vous pouvez l'associer à un `ContratLocation` via
	`contrat.set_mode_paiement(mode)` pour conserver l'information dans le contrat et la sérialiser.

## 7) Tests rapides non interactifs (optionnel)

Si vous préférez un test automatique, je peux ajouter un petit script qui crée des objets en dur, appelle la
méthode de sauvegarde, puis recharge et vérifie la présence des objets. Dites-moi si vous voulez que je l'ajoute.

## 8) Problèmes connus / améliorations possibles

- Validation des saisies (sélection d'index hors limites) peut être améliorée.
- Gestion d'identifiants uniques (ex : immatriculation) et de doublons non implémentée strictement.
- Le format de sérialisation est simple; pour une application réelle, envisager une base de données.

---

Faites-moi savoir si vous voulez que j'ajoute le script de test non interactif ou que j'améliore
la validation des entrées et les messages d'erreur.

