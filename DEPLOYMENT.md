# Guide de Déploiement

La mise en production de FootGolf Score nécessite trois environnements distincts : Développement, Staging (Recette) et Production.

## Prérequis de Production

- Un serveur avec Docker et Docker Compose.
- Un nom de domaine configuré (ex: `footgolf.example.ma`).
- Des certificats SSL (ex: Let's Encrypt).

## Docker Compose Production

Le fichier `docker-compose.prod.yml` doit inclure :
- Nginx (Reverse Proxy + SSL)
- Frontend (Next.js Standalone)
- Backend (FastAPI + Uvicorn)
- PostgreSQL (Base de données)

## Déploiement

1. Cloner le dépôt sur le serveur de production.
2. Configurer le fichier `.env.prod` avec des clés sécurisées générées aléatoirement :
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(64))"
   ```
3. Lancer la construction et le déploiement :
   ```bash
   docker compose -f docker-compose.prod.yml build
   docker compose -f docker-compose.prod.yml up -d
   ```
4. Exécuter les migrations de base de données :
   ```bash
   docker compose -f docker-compose.prod.yml exec backend alembic upgrade head
   ```

## HTTPS et WebSocket

Assurez-vous que Nginx redirige le port 443 correctement et configure les headers d'Upgrade pour supporter `wss://`. Le mode HTTPS est **obligatoire** pour que la PWA puisse être installée sur les appareils mobiles.
