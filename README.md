# 🔐 Auth-API — TP d’API d’Authentification

Ce projet fournit une API REST en Python/Flask pour gérer l’authentification et la gestion de profils utilisateurs, dans le cadre du TP « API d’authentification ».

## ⚙️ Prérequis

- Python 3.7+  
- WAMP / XAMPP ou MySQL installé  
- phpMyAdmin (facultatif)  
- Git, Postman (ou équivalent)

## 🚀 Installation & setup

1. **Cloner** le dépôt  
   ```bash
   git clone https://github.com/Gaye699/auth-api.git
   cd auth-api

## Créer et activer l’environnement virtuel
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# ou CMD
.\.venv\Scripts\activate.bat

## Installer les dépendances

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

## Crée la base de donnée via PhpMyAdmnin ou la console MySql

CREATE DATABASE user_auth_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE user_auth_db;

CREATE TABLE personne (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(100) NOT NULL,
  prenom VARCHAR(100),
  sexe CHAR(1) NOT NULL,
  date_naissance DATE NOT NULL,
  profession VARCHAR(100),
  email VARCHAR(150) NOT NULL UNIQUE,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  tel VARCHAR(20),
  active BOOLEAN DEFAULT TRUE
);

## Configurer config.py

SECRET_KEY      = 'votre_clef_flask'
JWT_SECRET_KEY  = 'info2-security'
MYSQL_HOST      = 'localhost'
MYSQL_USER      = 'root'
MYSQL_PASSWORD  = ''           # ou mdp de votre user MySQL
MYSQL_DB        = 'user_auth_db'

## Lancer l'API
python app.py

## Exemple sur Postman

*****Register****
![register](https://github.com/user-attachments/assets/4db7375a-b546-4c1d-851d-0359d9fe5237)

****Login*****
![login](https://github.com/user-attachments/assets/92548e99-c65a-4146-9e91-0e57886f8b54)

*****Profile*****
![user_profile](https://github.com/user-attachments/assets/ecb033ee-7d1a-4d26-b09f-933309ded18b)

*****Update*****
![update](https://github.com/user-attachments/assets/36cf4cfa-720d-484e-b0b6-a2961ce02067)

*****Desactivate-Profile*****
![profile-desactivate](https://github.com/user-attachments/assets/c15b2b40-0dbb-41ca-aca2-8cc0f86a5eae)


