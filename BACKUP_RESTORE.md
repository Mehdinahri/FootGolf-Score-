# Sauvegardes et Restauration

Il est crucial de sauvegarder régulièrement les données de l'application (Utilisateurs, Parcours, Scores). 

## Procédure de Sauvegarde (Backup)

Pour créer un dump SQL formaté et compressé :

```bash
docker compose -f docker-compose.prod.yml exec postgres pg_dump \
  -U footgolf_user \
  -d footgolf_db \
  -Fc \
  -f /backups/footgolf_$(date +%Y%m%d_%H%M).dump
```

*Note : Veillez à monter un volume externe ou un service de stockage cloud (S3) pour externaliser les fichiers générés dans `/backups/`.*

## Procédure de Restauration (Restore)

Pour restaurer une sauvegarde :

1. Assurez-vous que le service postgres tourne et que la base de destination existe.
2. Exécutez la restauration :

```bash
docker compose -f docker-compose.prod.yml exec postgres pg_restore \
  -U footgolf_user \
  -d footgolf_db \
  --clean \
  /backups/nom_du_fichier_backup.dump
```

**⚠️ Avertissement :** Le drapeau `--clean` effacera les tables existantes avant de restaurer les données. Procédez avec prudence.

## Tests Réguliers

Une sauvegarde non testée n'est pas fiable. Programmez une restauration mensuelle vers une base de test (`footgolf_restore_test`) pour vous assurer de l'intégrité de vos backups.
