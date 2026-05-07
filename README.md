# GreenLLM



https://github.com/user-attachments/assets/3a502337-14e5-4501-b458-eaec8ba1ce75


GreenLLM est une application qui combine :

- une API Spring Boot pour gerer les utilisateurs, entreprises, budgets, requetes, reponses, transactions et modeles LLM ;
- un service FastAPI Python pour calculer les scores carbone et router les requetes vers les modeles les plus adaptes ;
- une base H2 en memoire pour le developpement.
- un front en Vue.js pour les interactions avec l’utilisateur

## Architecture

```text
GreenLLM/
├── app/       # Backend Java Spring Boot
├── Router/    # Service Python FastAPI / LLM router
└── scr/       # Frontend Vue 
```

Par defaut :

- Spring Boot: `http://localhost:8080`
- FastAPI: `http://127.0.0.1:8000`
- Ollama: `http://127.0.0.1:55555`
- Vue Frontend: `http://localhost:5173`
- H2 Console: `http://localhost:8080/h2-console`
- Swagger Spring: `http://localhost:8080/swagger-ui/index.html`
- Swagger FastAPI: `http://127.0.0.1:8000/docs`

## Prerequis

- Java 21
- Maven ou le Maven Wrapper du projet
- Python 3.10+
- pip
- Node.js 18+
- npm


## Lancer le Router FastAPI

Depuis la racine :

```powershell
cd Router
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
uvicorn endpoint.api:main --reload
```

Verifier :

```text
http://127.0.0.1:8000/docs
```

Endpoints FastAPI principaux :

```http
GET /carbon?query=...
GET /utility-scores?query=...
```

## Lancer Spring Boot

Dans un autre terminal, depuis la racine :

```powershell
cd app
.\mvnw.cmd spring-boot:run
```

Si le wrapper Maven pose probleme :

```powershell
mvn spring-boot:run
```

Pour voir le detail d'une erreur :

```powershell
mvn spring-boot:run -e
```

## Base de Donnees H2

Configuration : `app/src/main/resources/application.properties`

```properties
spring.datasource.url=jdbc:h2:mem:greenllm
spring.datasource.username=sa
spring.datasource.password=
spring.h2.console.path=/h2-console
spring.jpa.hibernate.ddl-auto=update
```

Connexion H2 Console :

```text
JDBC URL: jdbc:h2:mem:greenllm
User: sa
Password: laisser vide
```

La table `ModelLLM` est automatiquement peuplee au demarrage dans `AppApplication.java`.
## Frontend (Vue 3)

### Stack technique

- [Vue 3](https://vuejs.org/) + Composition API
- [Vite](https://vitejs.dev/)
- [PrimeVue](https://primevue.org/) — bibliothèque de composants UI
- [Pinia](https://pinia.vuejs.org/) — gestion d’état
- [Vue Router](https://router.vuejs.org/) — routage côté client

### Vues

| Vue | Description |
|---|---|
| `LandingView` | Page d’accueil / point d’entrée |
| `LoginView` | Connexion utilisateur |
| `RegisterView` | Inscription utilisateur |
| `DashboardView` | Tableau de bord utilisateur individuel |
| `DashboardViewEMP` | Tableau de bord entreprise |
| `RoutingView` | Routeur LLM sensible à l’empreinte carbone |
| `CarbonView` | Estimation de l’empreinte carbone |
| `BudgetView` | Suivi du budget |
| `ReportsView` | Rapports d’utilisation |
| `ModelsView` | Modèles LLM disponibles |
| `AccountsView` | Gestion des comptes |
| `SettingsView` | Paramètres |

### Prérequis

- Node.js 18+
- npm

### Variables d’environnement

Créer un fichier `.env` à la racine du dossier `scr/` :

```text
VITE_API_BASE_URL=http://localhost:8080
VITE_OLLAMA_BASE_URL=http://127.0.0.1:55555
```

> Toutes les variables doivent être préfixées par `VITE_` afin d’être exposées par Vite.

### Installation et exécution

```powershell
cd scr
npm install
npm run dev
```

L’application sera disponible à l’adresse `http://localhost:5173`.

## Flux Front Typique

1. Creer ou connecter un utilisateur.
2. Appeler `POST /api/carbon` avec la query et l'utilisateur : Spring appelle FastAPI `/carbon`, recupere `input_tokens`, cree la requete, puis renvoie `requeteId`.
3. Appeler FastAPI `/utility-scores` via `POST /api/dashboard/stats` pour obtenir les scores par modele.
4. Utiliser ou enregistrer une reponse avec son nombre de tokens.
5. Creer une transaction avec `POST /api/transactions`.
6. Consulter les transactions et les budgets consommes.

Le cout d'une requete est calcule comme :

```text
input_cost = requete.nombreTokens * model.coutParToken
output_cost = reponse.nombreTokens * model.coutParToken
cout_total = input_cost + output_cost
```

## Auth Utilisateur

Creer un utilisateur :

```http
POST /api/auth/users/register
Content-Type: application/json
```

```json
{
  "email": "user@test.com",
  "prenom": "Ibrahim",
  "nom": "Test",
  "motDePasse": "secret",
  "statut": "EMPLOYE",
  "budget": 100,
  "adresse": {
    "rue": "Rue test",
    "ville": "Lyon",
    "codePostal": "69000",
    "pays": "France"
  }
}
```

Connexion :

```http
POST /api/auth/users/login
```

```json
{
  "email": "user@test.com",
  "motDePasse": "secret"
}
```

## Auth Entreprise

Creer une entreprise avec groupes et budgets :

```http
POST /api/auth/entreprises/register
```

```json
{
  "siret": "12345678900011",
  "domaine": "informatique",
  "motDePasse": "secret",
  "budget": 10000,
  "groupes": [
    {
      "description": "Equipe IA",
      "departement": "R&D",
      "niveauGroupe": 1,
      "budget": 3000
    }
  ]
}
```

Connexion entreprise :

```http
POST /api/auth/entreprises/login
```

```json
{
  "siret": "12345678900011",
  "motDePasse": "secret"
}
```

## Requetes

Creer une requete utilisateur :

```http
POST /api/requetes
```

```json
{
  "description": "Explique moi le RAG",
  "utilisateurId": 1
}
```

Ce endpoint ne demande plus le nombre de tokens. Le flux recommande pour les requetes venant du front est `POST /api/carbon`, car il cree la requete avec le vrai `input_tokens` retourne par FastAPI `/carbon`.

## Budget

Ajouter le cout d'une reponse au budget consomme d'un utilisateur :

```http
POST /api/budget/utilisateurs/{utilisateurId}/modeles/{modelId}/requetes/{requeteId}/reponses/{reponseId}/consommation
```

Calculer le cout economise d'un modele pour une requete/reponse :

```http
GET /api/budget/modeles/{modelId}/requetes/{requeteId}/reponses/{reponseId}/cout-economise
```

Resultat positif : le modele coute moins cher que la moyenne.

Resultat negatif : le modele coute plus cher que la moyenne.

## Transactions

Une transaction contient les details d'une consommation utilisateur :

- utilisateur ;
- modele utilise ;
- requete ;
- reponse ;
- cout ajoute ;
- budget consomme avant ;
- budget consomme apres ;
- date de creation.

Creer une transaction :

```http
POST /api/transactions
```

```json
{
  "utilisateurId": 1,
  "modelId": 2,
  "requeteId": 3,
  "reponseId": 4
}
```

Lister toutes les transactions :

```http
GET /api/transactions
```

Recuperer une transaction :

```http
GET /api/transactions/{transactionId}
```

Lister les transactions d'un utilisateur :

```http
GET /api/transactions/utilisateurs/{utilisateurId}
```

## Dashboard

Le dashboard Spring appelle FastAPI `/utility-scores`.

```http
POST /api/dashboard/stats
```

```json
{
  "query": "Explique moi le RAG"
}
```

Reponse attendue : liste de modeles avec score de performance et score CO2.

## FastAPI Router

Calcul carbone :

```http
GET http://127.0.0.1:8000/carbon?query=Explique%20moi%20le%20RAG
```

Proxy Spring avec creation de requete :

```http
POST /api/carbon
```

```json
{
  "query": "Explique moi le RAG",
  "utilisateurId": 1
}
```

La reponse Spring contient `requeteId`, `utilisateurId`, `inputTokens`, la liste `reponses` creee pour chaque modele de `carbon.models`, et la reponse brute FastAPI dans `carbon`.

Extrait :

```json
{
  "requeteId": 1,
  "utilisateurId": 1,
  "inputTokens": 10,
  "reponses": [
    {
      "reponseId": 1,
      "modelId": 2,
      "model": "GPT-4",
      "outputTokens": 100
    }
  ],
  "carbon": {}
}
```

Extrait de reponse :

```json
{
  "request_metrics": {
    "input_tokens": 10
  },
  "models": {
    "model-name": {
      "output_tokens_estimated": 100,
      "total_tokens": 110,
      "carbon_cost_per_token_kg_co2": 0.00000015,
      "total_carbon_cost_kg_co2": 0.0000165
    }
  }
}
```

Scores de routing :

```http
GET http://127.0.0.1:8000/utility-scores?query=Explique%20moi%20le%20RAG
```

## Modeles Seedes

Au demarrage, Spring insere ces modeles si absents :

| Modele | CO2/token | Cout/token |
|---|---:|---:|
| GPT-4 | 1.20 | 0.000045 |
| GPT-4o | 0.95 | 0.00000625 |
| GPT-4o-mini | 0.25 | 0.000000375 |
| Claude-3-opus | 1.10 | 0.000045 |
| Llama-3-70B | 0.60 | 0.000000625 |
| Llama-3-8B | 0.15 | 0.000000035 |

## Commandes Utiles

Compiler le backend :

```powershell
cd app
mvn clean compile
```

Lancer les tests :

```powershell
mvn test
```

Voir les logs detailles :

```powershell
mvn spring-boot:run -e
```

## Problemes Courants

Si Spring ne demarre pas avec une erreur Maven generique :

```text
Process terminated with exit code: 1
```

Relancer avec :

```powershell
mvn spring-boot:run -e
```

Si le dashboard ne repond pas, verifier que FastAPI tourne bien sur :

```text
http://127.0.0.1:8000
```

Si la base est vide apres redemarrage, c'est normal : H2 est configuree en memoire avec `jdbc:h2:mem:greenllm`.


[Open the PDF](pdfs/Rapport.pdf)
