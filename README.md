# FootGolf Score

Application web (PWA) de gestion des parties de FootGolf en temps réel.

## Vue d'ensemble

FootGolf Score remplace les cartes de score papier traditionnelles par une solution numérique complète. L'application permet la gestion des parcours, la saisie des scores hors-ligne ou en ligne, le calcul automatique des totaux, et propose un classement en temps réel des joueurs via WebSockets.

## Technologies

**Backend** : FastAPI, Python, PostgreSQL, SQLAlchemy, Alembic, WebSockets.
**Frontend** : Next.js 14, React, TypeScript, Tailwind CSS, TanStack Query, Dexie.js (IndexedDB).

## Fonctionnalités Principales

- Interface Administrateur pour la gestion des utilisateurs, des parcours (18 trous) et des parties.
- Interface Joueur mobile-first (PWA) pour la saisie de scores au fil du parcours.
- Synchronisation Hors-Ligne avec Dexie.js.
- Leaderboard en direct (WebSockets).

## Guide de Démarrage

Veuillez consulter le fichier [INSTALLATION.md](INSTALLATION.md) pour les instructions de mise en place de l'environnement de développement.

## Documentation

- [Guide d'Installation](INSTALLATION.md)
- [Guide de Déploiement](DEPLOYMENT.md)
- [Guide Utilisateur](USER_GUIDE.md)
- [Guide Administrateur](ADMIN_GUIDE.md)
- [Documentation API](API_DOCUMENTATION.md)
- [Sauvegardes et Restauration](BACKUP_RESTORE.md)
- [Sécurité](SECURITY.md)
- [Rapport de Tests](TEST_REPORT.md)
- [Notes de Version](RELEASE_NOTES.md)
