# Développement d'une API RESTFul
API permettant de remonter et suivre des problèmes techniques sur des projets.

## Description

L'API a pour but de :
* créer/modifier/supprimer des projets
* créer/modifier/supprimer des problèmes sur des projets
* créer/modifier/supprimer des commentaires sur des problèmes


## Se préparer à commencer

### Dépendances

* installer Windows, version 10.0.19043
* installer Python 3.10

### Installation

* git clone https://github.com/BastienDslnds/oc_python_projet_10.git
* Créer et activer l'environnement virtuel 
  * 1- ouvrir l'application "invite de commande"
  * 2- se positionner dans le dossier "oc_python_projet_10"
  * 3- créer l'environnement virtuel avec: "python -m venv .venv"
  * 4- Activer l'environnement virtuel avec: "source .venv/Scripts/activate"
  * 5- utiliser la commande suivante pour installer les packages: "pip install -r requirements.txt"

### Lancer l'application Web

* Se positionner dans le dossier "issuetracking" avec: "cd issuetracking"
* Lancer l'application web avec: "python manage.py runserver"


### Documentation de l'API

* Lien vers la documentation Postman de l'API: https://documenter.getpostman.com/view/22963855/2s8ZDYZ2md 


## Auteurs

Bastien Deslandes

bastien.deslandes@free.fr