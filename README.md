### API Clients - Documentation

#### Contexte
L'API Clients gère les informations des clients et assure leur stockage et récupération. Elle est conçue pour interagir avec les API Produits et Commandes pour des opérations synchronisées via RabbitMQ, servant ainsi de base de données de clients pour l'ensemble du système.

#### Prérequis
- **Python 3.9+**
- **Docker** et **Docker Compose** installés
- **RabbitMQ** en cours d'exécution avec le réseau Docker partagé `backend` (se référer à la [documentation](https://github.com/Cortexico/MSPR-RabbitMQ))
- Fichier `.env` correctement configuré avec les variables suivantes :

```plaintext
POSTGRES_USER=customers
POSTGRES_PASSWORD=apiCustomers
POSTGRES_DB=customers_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

API_HOST=0.0.0.0
API_PORT=8000

RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
```

#### Instructions de démarrage
#### **1. Cloner le dépôt de l'API Clients** :
   ```bash
   git clone https://github.com/Cortexico/MSPR-API-Clients.git
   ```
#### **2. Créer le réseau Docker partagé** (si non existant) :
   ```bash
   docker network create backend
   ```
#### **3. Créer un Environnement Virtuel**

Il est recommandé d'utiliser un environnement virtuel pour isoler les dépendances.

- **Sur Windows :**
  Création de l'environnement virtuel:
   ```bash
   python -m venv venv
   ```
  
  Lancement de l'environnement virtuel: 
   ```bash
   venv\Scripts\activate
   ```

- **Sur macOS/Linux :**

   Création de l'environnement virtuel:
   ```bash
   python3 -m venv venv
   ```
   
   Lancement de l'environnement virtuel:
   ```bash
   source venv\Scripts\activate
   ```

#### **4. Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
#### **5. Lancer l’API avec Docker Compose** :
   ```bash
   docker-compose up --build
   ```
   - Cette commande va construire les images Docker et lancer les services définis dans `docker-compose.yml`, y compris la base de données PostgreSQL.
   
#### **6. Pour arrêter et supprimer les volumes Docker** (si nécessaire) :
   ```bash
   docker-compose down -v
   ```
#### **Sans Docker**

**1. Lancer la Base de Données PostgreSQL**

- Assurez-vous que PostgreSQL est installé et en cours d'exécution.
- Créez une base de données et un utilisateur correspondant aux variables d'environnement.

**2. Lancer l'API**

```bash
uvicorn app.main:app --host ${API_HOST} --port ${API_PORT}
```

#### **Accès à la Documentation de l'API**

- Une fois l'API lancée, accédez à la documentation interactive :

  ```
  http://localhost:8000/docs
  ```

#### Documentation technique de l'API

##### Endpoints principaux
- **GET /customers** : Récupère la liste des clients.
  - **Réponse** : JSON array avec les informations de chaque client.
  
- **POST /customers** : Ajoute un nouveau client.
  - **Corps** : JSON contenant `name`, `email`, `address`.
  - **Réponse** : Confirmation de création avec les détails du client ajouté.
  
- **GET /customers/{id}** : Récupère les détails d’un client spécifique.
  - **Paramètre** : `id` de l’utilisateur.
  - **Réponse** : Détails du client en JSON.
  
- **PUT /customers/{id}** : Met à jour les informations d’un client.
  - **Corps** : JSON avec les champs à mettre à jour.
  - **Réponse** : Détails mis à jour du client.
  
- **DELETE /customers/{id}** : Supprime un client.
  - **Paramètre** : `id` de l’utilisateur.
  - **Réponse** : Confirmation de suppression.

##### Services RabbitMQ
L'API utilise RabbitMQ pour publier et consommer des messages liés aux mises à jour de données des clients.

- **Publisher** : Envoie des messages lors de la création ou modification de clients.
- **Consumer** : Réception et gestion de messages pertinents provenant des autres API (Produits et Commandes).

## **Notes Importantes pour Toutes les APIs**

### **Fichiers `.env`**

- Les fichiers `.env` sont essentiels pour le fonctionnement des APIs.
- Ils contiennent les variables d'environnement nécessaires à la configuration des bases de données et des services externes.
- Assurez-vous que ces fichiers sont placés à la racine de chaque projet.

### **Docker Compose**

- L'utilisation de Docker Compose est recommandée pour faciliter le déploiement des services dépendants comme les bases de données et RabbitMQ.
- Les commandes `docker-compose up --build` et `docker-compose down -v` permettent de gérer facilement les conteneurs.

### **Gestion des Dépendances**

- Les fichiers `requirements.txt` listent toutes les dépendances Python nécessaires.
- Après avoir activé l'environnement virtuel, installez les dépendances avec :

  ```bash
  pip install -r requirements.txt
  ```

### **Résolution des Problèmes Courants**

- **Ports Occupés :**

  - Si un port est déjà utilisé, modifiez la variable `API_PORT` dans le fichier `.env` et ajustez les ports exposés dans le `docker-compose.yml`.

- **Problèmes de Connexion aux Bases de Données :**

  - Vérifiez que les services de base de données sont en cours d'exécution.
  - Assurez-vous que les variables d'environnement correspondent aux configurations de vos services.

- **Erreurs lors de l'Activation de l'Environnement Virtuel :**

  - Assurez-vous que vous utilisez la bonne version de Python.
  - Vérifiez les permissions du dossier `venv`.

### **Documentation et Tests**

- Chaque API est fournie avec une documentation interactive accessible via `/docs`.
- Utilisez cet outil pour tester les endpoints et comprendre les modèles de données.

### **Sécurité**

- **Variables Sensibles :**

  - Ne partagez pas vos fichiers `.env` ou toute information sensible.
  - Pour un environnement de production, utilisez des gestionnaires de secrets sécurisés.

- **Mises à Jour :**

  - Gardez vos dépendances à jour en vérifiant régulièrement le fichier `requirements.txt`.
  
