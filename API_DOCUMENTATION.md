# Documentation API

L'API de FootGolf Score est construite avec **FastAPI** et suit le standard OpenAPI (Swagger).

## Swagger UI

Une fois le backend lancé, la documentation interactive est disponible sur :
- `http://localhost:8000/docs` (Environnement local)
- `https://api.footgolf.example.ma/docs` (Production, si activé)

## Endpoints Principaux

### Authentification (`/api/v1/auth`)
- `POST /login` : Fournit l'email et le mot de passe, retourne l'Access Token et le Refresh Token.
- `POST /refresh` : Renouvelle l'Access Token.
- `GET /me` : Récupère les informations de l'utilisateur connecté.

### Parcours (`/api/v1/courses`)
- `GET /` : Liste des parcours.
- `POST /` : Crée un parcours (Admin).
- `GET /{id}` : Détails d'un parcours et de ses 18 trous.

### Parties (`/api/v1/games`)
- `GET /` : Liste des parties.
- `POST /` : Crée une partie (Admin).
- `POST /{id}/register` : Le joueur s'inscrit à une partie.
- `POST /{id}/scores` : Enregistre le score d'un trou.
- `GET /{id}/scorecard` : Récupère l'état complet de la carte de score du joueur.
- `GET /{id}/leaderboard` : Récupère le classement actuel.

### Hors-Ligne (`/api/v1/offline-sync`)
- `POST /scores` : Endpoint idempotent de synchronisation en lots (Batch Sync). Accepte un tableau de scores contenant une `idempotency_key` pour éviter les doublons de synchronisation.

### WebSockets (`/ws/games`)
- `WS /{id}/leaderboard` : Connexion WebSocket pour recevoir les événements `LEADERBOARD_UPDATE` en direct. Authentification via token JWT en query param.
