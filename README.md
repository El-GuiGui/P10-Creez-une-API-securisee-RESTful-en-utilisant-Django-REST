# Projet 10 - Créez une API sécurisée RESTful en utilisant Django REST

# SoftDesk 
SoftDesk est une application de remontée et suivi des problèmes techniques destinée aux entreprises en B2B. Cette API RESTful a été développée en utilisant Django et Django REST Framework.

![image](https://github.com/El-GuiGui/P10-Creez-une-API-securisee-RESTful-en-utilisant-Django-REST/assets/148984263/0ed9fd2a-0186-4d1f-bd5a-de3eb5534ced)


## Table des Matières

- [Mise en Place et Installation](#mise-en-place-et-installation)
- [Fonctionnalités](#fonctionnalités)
- [Utilisateurs par Défaut](#utilisateurs-par-défaut)
- [Endpoints de l'API](#endpoints-de-lapi)
- [Green Code](#green-code)
- [Sécurité](#sécurité)
- [Respect du RGPD](#respect-du-rgpd)







## Mise en Place et Installation

### Prérequis

- Python 3.7 ou supérieur
- Pipenv (pour la gestion des dépendances)


### Installation


1. Clonez le dépôt Git sur votre machine locale :

    ```bash
    git clone https://github.com/El-GuiGui/P10-Creez-une-API-securisee-RESTful-en-utilisant-Django-REST.git
    ```

    ```bash
    cd P10-Creez-une-API-securisee-RESTful-en-utilisant-Django-REST
    ```



2. Installer Pipenv :
    ```bash
    pip install pipenv
    ```

3. Créer et activer l'environnement virtuel avec Pipenv :
    ```bash
    pipenv install
    ```
    
    ```bash
    pipenv shell
    ```

4. Installer les dépendances définies dans le `Pipfile` :
    ```bash
    pipenv install
    ```


5. Appliquer les migrations :
    ```bash
    python manage.py migrate
    ```

4. Lancez le serveur de développement :

    ```bash
    python manage.py runserver
    ```

5. Accédez à l'application via votre navigateur à l'adresse suivante : `http://127.0.0.1:8000/`



## Fonctionnalités

- **Gestion des Utilisateurs :**
  - Inscription avec collecte des informations de consentement (contact et partage de données).
  - Authentification via JSON Web Token (JWT).
  - Suppression de compte utilisateur avec anonymisation des données liées.

- **Gestion des Projets :**
  - Création, modification et suppression de projets.
  - Attribution de contributeurs aux projets.

- **Gestion des Issues :**
  - Création, modification et suppression des issues.
  - Assignation des issues à des utilisateurs spécifiques.
  - Priorisation et catégorisation des issues.

- **Gestion des Commentaires :**
  - Ajout de commentaires aux issues.
  - Modification et suppression des commentaires par leur auteur.


## Utilisateurs par Défaut

### Admin

- **Nom d'utilisateur :** `admin`
- **Mot de passe :** `sofdesk`

### Autres :

- **Nom d'utilisateur :** `john`
- **Mot de passe :** `johnsoft123`

## Remarque :
### Modèle UserProfile

Plutôt que de redéfinir complètement le modèle `User` de Django, un modèle `UserProfile` a été créé pour étendre les fonctionnalités du modèle `User` par défaut. Cette approche a été choisie pour conserver la compatibilité avec les fonctionnalités intégrées de Django et pour permettre une plus grande flexibilité. Le modèle `UserProfile` contient des informations supplémentaires telles que la date de naissance et les consentements de l'utilisateur.

### Attributs du modèle UserProfile

- **user** : Référence au modèle `User`.
- **birth_date** : Date de naissance de l'utilisateur.
- **can_be_contacted** : Consentement de l'utilisateur pour être contacté.
- **can_data_be_shared** : Consentement de l'utilisateur pour le partage de ses données.

## Endpoints de l'API

### Authentification

- `POST /api/token/`: Obtenir un token JWT.
- `POST /api/token/refresh/`: Rafraîchir un token JWT.

### Utilisateurs

- `POST /register/`: Inscription d'un nouvel utilisateur.
- `DELETE /delete/`: Suppression du compte utilisateur.

### Projets

- `GET /projects/`: Liste des projets.
- `POST /projects/`: Création d'un projet.
- `GET /projects/{id}/`: Détails d'un projet.
- `PUT /projects/{id}/`: Mise à jour d'un projet.
- `DELETE /projects/{id}/`: Suppression d'un projet.

### Contributeurs

- `GET /contributors/`: Liste des contributeurs.
- `POST /contributors/`: Ajout d'un contributeur.
- `GET /contributors/{id}/`: Détails d'un contributeur.
- `PUT /contributors/{id}/`: Mise à jour d'un contributeur.
- `DELETE /contributors/{id}/`: Suppression d'un contributeur.

### Issues

- `GET /issues/`: Liste des issues.
- `POST /issues/`: Création d'une issue.
- `GET /issues/{id}/`: Détails d'une issue.
- `PUT /issues/{id}/`: Mise à jour d'une issue.
- `DELETE /issues/{id}/`: Suppression d'une issue.

### Commentaires

- `GET /comments/`: Liste des commentaires.
- `POST /comments/`: Création d'un commentaire.
- `GET /comments/{id}/`: Détails d'un commentaire.
- `PUT /comments/{id}/`: Mise à jour d'un commentaire.
- `DELETE /comments/{id}/`: Suppression d'un commentaire.

## Green Code

Pour réduire l'impact environnemental de l'application, plusieurs mesures ont été implémentées :

- **Pagination :** Toutes les listes de ressources utilisent la pagination pour réduire la charge sur le serveur.
- **Optimisation des Requêtes :** Les requêtes ont été optimisées pour éviter la surconsommation des ressources du serveur.

## Sécurité

- **Authentification :** Utilisation de JWT pour sécuriser les endpoints de l'API.
- **Permissions :** Seuls les utilisateurs authentifiés peuvent accéder aux ressources. Les permissions sont gérées pour s'assurer que seuls les utilisateurs concernés peuvent modifier ou supprimer leurs propres publications.
- **Mise à jour et Suppression :** Les utilisateurs ne peuvent modifier ou supprimer que leurs propres projets, issues, et commentaires.

## Respect du RGPD et de l'OWASP

- **Collecte de l'âge et des consentements :** Lors de l'inscription, l'âge de l'utilisateur et les consentements pour être contacté et partager des données sont collectés.
- **Droit à l'oubli :** Les utilisateurs peuvent supprimer leur compte et leurs données personnelles seront anonymisées dans les objets liés (comme les commentaires et les projets).
- **Accès et Rectification :** Les utilisateurs peuvent accéder et mettre à jour leurs informations personnelles.

---


### Note : 



Je rajoute ici les rapports de flake8 pour la conformité de la pep8 :
![reportflake](image.png)