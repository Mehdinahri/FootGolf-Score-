# Guide d'Installation

## Prérequis

- Docker et Docker Compose
- Node.js 20+
- Python 3.12+

## Installation Locale (Développement)

### Backend

1. Naviguer dans le dossier `backend`.
2. Créer un environnement virtuel : `python -m venv venv`
3. Activer l'environnement : `source venv/bin/activate` (ou `venv\Scripts\activate` sous Windows)
4. Installer les dépendances : `pip install -r requirements.txt`
5. Créer un fichier `.env` basé sur les spécifications.
6. Démarrer la base de données via Docker : `docker-compose up -d postgres`
7. Lancer les migrations : `alembic upgrade head`
8. Démarrer le serveur : `uvicorn app.main:app --reload`

### Frontend

1. Naviguer dans le dossier `frontend`.
2. Installer les dépendances : `npm install`
3. Créer un fichier `.env.local` basé sur `.env.example`.
4. Démarrer le serveur de développement : `npm run dev`

L'application sera accessible sur `http://localhost:3000` et l'API sur `http://localhost:8000`.
