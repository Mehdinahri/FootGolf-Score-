# Plan d'Implémentation Frontend (Étape 6)

Ce plan détaille la construction de l'application frontend Next.js pour FootGolf Score.

## Objectif

Développer une PWA mobile-first avec Next.js App Router, connectée à l'API FastAPI, permettant la gestion complète du FootGolf (connexion, administration, saisie des scores, classement en direct, et support hors-ligne).

## User Review Required

> [!IMPORTANT]  
> Bien que nous commencions le développement frontend, **l'API backend complète (parcours, parties, scores, websockets) n'a pas encore été implémentée** (nous nous étions arrêtés à l'authentification à l'étape 2).
> 
> *Question* : Souhaitez-vous que je génère le frontend avec des appels API pointant vers les endpoints prévus (qui retourneront des erreurs 404 tant que le backend n'est pas complété), ou voulez-vous que je développe d'abord les endpoints FastAPI manquants (Étapes 3, 4, 5) avant de faire le frontend ?

## Technologies et Bibliothèques

- **Framework** : Next.js 15 (App Router), React 19, TypeScript
- **Styling** : Tailwind CSS, Lucide React (icônes), Tailwind Merge, clsx
- **Formulaires & Validation** : React Hook Form, Zod, @hookform/resolvers
- **State & Data Fetching** : TanStack Query (React Query) v5, Axios
- **Offline & Stockage** : Dexie.js (IndexedDB wrapper)
- **WebSockets** : API native `WebSocket` + hook React custom

## Structure du Projet (App Router)

L'arborescence suivra la proposition initiale de l'Étape 1 :

```text
frontend/
├── app/
│   ├── (auth)/login/page.tsx
│   ├── (dashboard)/
│   │   ├── dashboard/page.tsx
│   │   ├── games/[id]/scorecard/page.tsx
│   │   ├── games/[id]/leaderboard/page.tsx
│   │   └── ...
│   ├── (admin)/
│   │   ├── admin/courses/page.tsx
│   │   ├── admin/games/page.tsx
│   │   └── ...
│   ├── layout.tsx
│   └── globals.css
├── components/
│   ├── ui/ (Button, Input, Card, Modal, etc.)
│   ├── auth/ (LoginForm, ProtectedRoute)
│   ├── game/ (GameCard, PlayerList)
│   ├── score/ (ScoreEntry, HoleNavigator)
│   └── leaderboard/ (LeaderboardTable)
├── features/ (Logique métier, hooks React Query par domaine)
│   ├── auth/
│   ├── courses/
│   ├── games/
│   └── scores/
├── lib/
│   ├── api.ts (Axios instance avec intercepteurs pour JWT)
│   ├── queryClient.ts
│   ├── offlineDb.ts (Dexie database config)
│   └── utils.ts (cn, formatage)
└── types/ (Interfaces TypeScript correspondantes aux schémas backend)
```

## Étapes de Développement Proposées

1. **Initialisation** : `npx create-next-app@latest`, installation des dépendances (Tailwind, Zod, React Query, Dexie, Axios).
2. **Configuration Core** : Instance Axios avec intercepteurs de refresh token, QueryClient provider, Dexie DB.
3. **Composants UI de base** : Boutons, Inputs, Cartes, Modals (Mobile-first, gros boutons).
4. **Authentification** : Page de login, Context Auth, Protection des routes côté client.
5. **Espace Admin** : Gestion des parcours (trous) et création de parties.
6. **Espace Joueur** : Liste des parties, Inscription.
7. **Écran de Saisie des Scores** : Interface mobile avec gros boutons +/- pour strokes et penalties, indicateur de synchronisation, Dexie fallback hors-ligne.
8. **Classement en Direct** : Intégration WebSocket.

## Verification Plan

- Le projet Next.js compile sans erreurs TypeScript.
- Le design est responsive (testable via les DevTools du navigateur en mode mobile).
- La connexion JWT fonctionne avec le backend existant.
