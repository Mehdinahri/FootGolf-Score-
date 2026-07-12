# Sécurité de l'Application

La sécurité est un pilier de FootGolf Score.

## Authentification et Autorisation
- **JWT (JSON Web Tokens)** : Les tokens ont une durée de vie courte (15 minutes).
- **Refresh Token** : Valide 7 jours, il permet de renouveler l'accès de façon transparente, sans exposer un token long terme à des attaques.
- **Rôles** : Une séparation stricte existe entre le rôle `USER` et `ADMIN`. Seuls les admins peuvent altérer les parcours et configurer les parties.

## Protection des Données Sensibles
Les secrets et mots de passe ne sont **jamais** exposés ni journalisés :
- Les mots de passe sont hachés (Bcrypt).
- Les clés JWT (`JWT_SECRET_KEY`) doivent être générées via un outil de cryptographie sécurisé pour l'environnement de production.

## Réseau
- **HTTPS Obligatoire** : Toutes les communications frontend/backend en production doivent passer par SSL/TLS pour prévenir le *Man-In-The-Middle*. Les WebSockets utilisent `wss://`.
- **CORS** : Les origines sont strictement limitées dans le backend via `CORS_ORIGINS` (ex: `https://footgolf.example.ma`).

## Vulnérabilités Web
- Injection SQL prévenue nativement par l'utilisation de l'ORM SQLAlchemy.
- Validation Pydantic / Zod aux deux extrémités (Frontend et Backend) pour se protéger contre les charges utiles malveillantes.
