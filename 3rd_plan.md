# Plan d'Implémentation Backend (Phase 1 à 8)

Ce plan décrit les étapes nécessaires pour compléter le backend FastAPI afin qu'il réponde aux attentes du frontend Next.js nouvellement créé, incluant la gestion des entités, le classement en temps réel via WebSockets, et la synchronisation hors ligne.

## Matrice des Contrats API (Inspection de l'Existant)

Voici l'inspection des appels actuellement effectués par le frontend Next.js par rapport au backend existant, ainsi que les routes à créer :

| Fonction | Appel Frontend Actuel | Route Backend Attendue (v1) | Statut / Action |
|----------|------------------------|------------------------------|-----------------|
| **Login** | `POST /auth/login` | `POST /api/v1/auth/login` | ✅ Existant et fonctionnel |
| **Mon profil** | `GET /auth/me` | `GET /api/v1/auth/me` | ✅ Existant et fonctionnel |
| **Rafraîchir** | `POST /auth/refresh` | `POST /api/v1/auth/refresh` | ✅ Existant et fonctionnel |
| **Liste Parties (Publique)** | `GET /games` | `GET /api/v1/games` | ❌ À créer |
| **Liste Parties (Admin)** | `GET /admin/games` | `GET /api/v1/admin/games` | ❌ À créer |
| **Liste Parcours** | `GET /courses` | `GET /api/v1/courses` | ❌ À créer |
| **Carte de Score** | *(Non encore codé dans l'UI, prévu)* | `GET /api/v1/games/{id}/scorecard` | ❌ À créer |
| **Sauvegarde Score** | *(Non encore codé dans l'UI, prévu)* | `POST /api/v1/games/{id}/scores` | ❌ À créer |
| **Classement** | `GET /games/{id}/leaderboard` | `GET /api/v1/games/{id}/leaderboard` | ❌ À créer |
| **WebSocket Classement**| `WS /ws/games/{id}?token=...` | `WS /api/v1/ws/games/{id}` | ❌ À créer |
| **Sync Hors-Ligne** | *(Non encore codé)* | `POST /api/v1/offline-sync/scores` | ❌ À créer |

> [!TIP]
> **Alignement des préfixes :**
> L'instance Axios du Frontend est configurée avec `baseURL: "http://localhost:8000/api/v1"`. Tous les appels de la colonne "Appel Frontend Actuel" sont donc automatiquement préfixés par `/api/v1` en arrivant sur le Backend. Le contrat est donc parfaitement aligné.

## Stratégie d'Architecture Backend

Nous allons conserver l'architecture actuelle propre et modulaire. Le découpage sera le suivant :
- **Models** : SQLAlchemy (Déjà créés à l'Étape 2).
- **Schemas** : Pydantic (Déjà créés à l'Étape 2).
- **Repositories** : Abstraction de l'accès DB (ex: `CourseRepository`, `GameRepository`).
- **Services** : Logique métier et transactions (ex: `ScoreCalculationService`, `GameStatusService`, `TiebreakerService`, `OfflineSyncService`).
- **Websocket** : `ConnectionManager` dédié à la diffusion par partie.
- **API Routers** : Point d'entrée HTTP très fin qui délègue aux services (`app/api/v1/routers/...`).

## User Review Required

> [!IMPORTANT]
> Avant de démarrer l'implémentation (Phases 2 à 7), veuillez valider cette matrice d'intégration et l'architecture proposée.
>
> Êtes-vous d'accord pour que je commence par la **Phase 2** (Implémentation du CRUD Parcours, Trous, Parties et Inscriptions) et que j'écrive les tests pytest correspondants ?
