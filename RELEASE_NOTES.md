# Release Notes - v1.0.0

**Date de publication :** 12 Juillet 2026
**Version :** 1.0.0 (Release Candidate Stable)

## Fonctionnalités Introduites

### Plateforme Core
- Architecture Monolithique Modulaire avec FastAPI (Backend) et Next.js 14 App Router (Frontend).
- Base de données PostgreSQL centralisée pour la persistance complète des parcours, trous, parties et scores.

### Backend
- **Sécurité** : Intégration JWT complète avec mécanisme de Refresh Token.
- **WebSocket** : Serveur de push intégré pour l'actualisation du classement.
- **Mode Hors-ligne** : Endpoint d'ingestion massive (`/offline-sync/scores`) basé sur l'idempotence pour prévenir les doublons lors des reconnexions.
- **Règles métier** : Blocage de l'inscription si plus de 5 joueurs. Vérification stricte des trous et des parties.

### Frontend
- **Interface Mobile-First** : Carte de score responsive, ergonomique pour une saisie rapide à une main sur les parcours.
- **PWA (Progressive Web App)** : Le frontend est installable avec Service Worker (`sw.js`) pour le cache des ressources statiques et un "Fallback" réseau (Network Status).
- **Stockage Local** : Mise en place de Dexie.js pour mettre en file d'attente les saisies sans connexion internet.
- **WebSockets** : Classement instantané (Leaderboard) sur la partie active.

## Prochaines Étapes
- Phase de Test Terrain ("Recette").
- Déploiement en Staging puis en Production finale avec certificats SSL et isolation réseau complète.
