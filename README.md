# Système de Gestion de Stock et Produits (API REST)

Ce projet consiste en un système de gestion d'inventaire et de produits automatisé, développé sous forme d'API REST résiliente. Conçu initialement pour répondre aux besoins d'organisation des flux logistiques et de stockage d'entreprise, ce système a été entièrement optimisé pour s'exécuter dans des environnements aux ressources matérielles restreintes.

## 🚀 Caractéristiques du Projet

- **Architecture Backend Légère :** Développé en Python avec le micro-framework Flask, garantissant des performances rapides et une consommation minimale de mémoire.
- **Persistance des Données (SQL) :** Intégration d'une base de données relationnelle SQLite, utilisant des requêtes SQL pures pour la création de tables et les opérations de manipulation de données.
- **Opérations CRUD Complètes :** Gestion totale des produits (Création, Lecture, Mise à jour et Suppression) via des points de terminaison (Endpoints) API standardisés au format JSON.
- **Optimisation Linux & CLI :** Système entièrement configuré, testé et exécuté via l'interface en ligne de commande (Terminal CLI) sous un environnement Linux.

## 🛠️ Technologies Utilisées

- **Langage :** Python 3
- **Framework Web :** Flask
- **Base de Données :** SQLite (SQL)
- **Environnement de Déploiement :** Linux / CLI (Termux)

## 📌 Endpoints de l'API (Architecture REST)

| Méthode | Action | Endpoint | Corps de la Requête (JSON) |
| :--- | :--- | :--- | :--- |
| **POST** | Ajouter un produit | `/produtos` | `{"nome": "Produit", "quantidade": 10, "preco": 150.0}` |
| **GET** | Lister tous les produits | `/produtos` | Aucun |
| **PUT** | Modifier un produit par ID | `/produtos/<id>` | `{"nome": "Nouveau Nom", "quantidade": 5, "preco": 160.0}` |
| **DELETE** | Supprimer un produit par ID | `/produtos/<id>` | Aucun |

## 💻 Comment Exécuter le Projet Localement

1. **Initialiser la base de données SQL :**
```bash
   python database.py

