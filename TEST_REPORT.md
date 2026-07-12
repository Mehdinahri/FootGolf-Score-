# Rapport de Tests - Version 1.0.0

## Résumé
L'application dispose d'une infrastructure de test complète pour certifier sa stabilité en production. Tous les tests sont validés pour la RC (Release Candidate).

## Backend (Pytest)
Couverture des cas :
- Validation des inscriptions avec limite de 5 joueurs.
- Gestion d'erreurs (404, 422, 403, 401).
- Validation du calcul algorithmique du leaderboard.
- Synchronisation idempotente (simulation de renvois multiples hors-ligne).

## Frontend (Vitest)
Tests unitaires ciblés sur les logiques métier et les transformateurs :
- L'intercepteur Axios `normalizeApiError` a été testé avec succès.
- Les appels hors-ligne sont conformes.

## End-to-End (Playwright)
Validations transverses simulant un navigateur :
- Exécution réussie sur Chromium et Mobile Chrome.
- Routage et restrictions des routes d'authentification (`/login` vers `ProtectedRoute`).
- Conformité du titre et des éléments visuels cruciaux.

Les tests automatisés démontrent que la logique fondamentale est saine. Les futurs tests devront se concentrer sur la **Recette Utilisateur (UAT)** en conditions réelles (en plein soleil, avec une connexion cellulaire fluctuante).
