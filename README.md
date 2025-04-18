# 🌱 EcoShop - API REST pour produits électroménagers écoresponsables

_EcoShop est un projet backend qui fournit une API REST avec des informations sur des produits électroménagers extraits d'Amazon. Les produits sont classés selon différents critères écologiques._

---

## 🚀 Fonctionnalités

- 🔄 Récupération de données triées par :
  - 💸 **Prix**
  - 🌍 **Indice écologique**
  - 🏷️ **Nom** / 📦 **Catégorie**

---
🔏 Authentifcaiton : 
   -**Un système d'authentification d'utilisateur basé sur les jetons jwt pour sécuriser l'accès des utilisateurs**

## 🛠️ Technologies utilisées

- 🐘 **PostgreSQL** : base de données hébergée sur [Railway.app](https://railway.app)
- 🌐 **Django REST Framework** : pour une API robuste et sécurisée
- ⚙️ **Django** : framework backend principal
- 🕸️ **ScrapAPI** : extraction des produits depuis Amazon
- 🧠 **OpenAI** : génération automatique d’informations manquantes sur les produits
-  🔑 **JWT (JSON Web Token)** : pour sécuriser les endpoints de l'API
---

## 📦 Objectif du projet

Ce projet vise à faciliter la **découverte de produits électroménagers plus durables** en centralisant et en structurant les données environnementales liées à chaque article.

---

## 📸 Exemple de requête

```navigateur 
https://projetfac-ecoshop-aba0e7285826.herokuapp.com/produits/?api_key=Ecoshop2025
