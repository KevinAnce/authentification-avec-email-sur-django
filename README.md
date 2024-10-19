
# Utilisation d’adresse e-mail pour l’authentification avec DJANGO

## Description

Ceci est une application Django personnalisée où l'authentification des utilisateurs se fait par adresse email plutôt que par nom d'utilisateur. L'application inclut des fonctionnalités de connexion, déconnexion, inscription.

## Prérequis

Avant de lancer l'application, assure-toi d'avoir installé les éléments suivants :

- **Python 3.x**
- **pip** (gestionnaire de paquets Python)
- **Virtualenv** (facultatif mais recommandé pour isoler l'environnement Python)

## Installation

### 1. Cloner le dépôt

Commence par cloner le dépôt GitHub sur ton ordinateur local :

```bash
git clone https://github.com/KevinAnce/authentification-avec-email-sur-django.git
cd authentification-avec-email-sur-django
```

### 2. Créer et activer un environnement virtuel

Il est recommandé d'utiliser un environnement virtuel pour isoler les dépendances du projet. Voici comment créer et activer l'environnement virtuel :

```bash
# Créer l'environnement virtuel
python3 -m venv .venv

# Activer l'environnement virtuel (Linux/macOS)
source .venv/bin/activate

# Activer l'environnement virtuel (Windows)
.venv\Scripts\activate
```

### 3. Installer les dépendances

Installe les dépendances du projet listées dans le fichier `requirements.txt` :

```bash
pip install -r requirements.txt
```

### 4. Configurer la base de données

Applique les migrations pour configurer la base de données :

```bash
python manage.py migrate
```

### 5. Créer un super utilisateur

Pour accéder à l'administration Django, crée un super utilisateur avec la commande suivante :

```bash
python manage.py createsuperuser
```

### 6. Lancer le serveur de développement

Une fois les étapes précédentes complétées, tu peux lancer le serveur de développement local :

```bash
python manage.py runserver
```

L'application sera disponible à l'adresse suivante : `http://localhost:8000/`.
