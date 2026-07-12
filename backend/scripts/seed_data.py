"""
Script pour peupler la base de données avec des données initiales.

- 1 administrateur
- 5 joueurs de test
- 1 parcours (18 trous)
- 3 parties (DRAFT, REGISTRATION_OPEN, IN_PROGRESS avec scores)
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from datetime import date, datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from app.models import *

def seed_db(db: Session) -> None:
    print("Début du seeding de la base de données...")

    # 1. Création Admin
    admin = db.query(User).filter_by(email=settings.ADMIN_EMAIL).first()
    if not admin:
        print("Création de l'administrateur...")
        admin = User(
            first_name=settings.ADMIN_FIRST_NAME,
            last_name=settings.ADMIN_LAST_NAME,
            email=settings.ADMIN_EMAIL,
            password_hash=security.hash_password(settings.ADMIN_PASSWORD),
            role=UserRole.ADMIN,
        )
        db.add(admin)

    # 2. Création Joueurs
    players = []
    for i in range(1, 6):
        email = f"joueur{i}@footgolf.com"
        player = db.query(User).filter_by(email=email).first()
        if not player:
            print(f"Création du joueur {i}...")
            player = User(
                first_name="Joueur",
                last_name=str(i),
                email=email,
                password_hash=security.hash_password("password"),
                role=UserRole.PLAYER,
            )
            db.add(player)
        players.append(player)
    db.commit()

    # Recharge les entités (au cas où elles viennent d'être créées)
    admin = db.query(User).filter_by(email=settings.ADMIN_EMAIL).first()
    players = db.query(User).filter(User.role == UserRole.PLAYER).all()

    # 3. Création Parcours & Trous
    course = db.query(Course).first()
    if not course:
        print("Création du parcours de test...")
        course = Course(
            name="Paris FootGolf Club",
            city="Paris",
            hole_count=18,
            par_total=71,
            distance_total=2400,
            description="Parcours officiel pour les compétitions.",
        )
        db.add(course)
        db.commit()
        db.refresh(course)

        print("Création des 18 trous...")
        pars = [5, 4, 3, 4, 4, 3, 5, 4, 4, 4, 3, 5, 4, 4, 3, 4, 4, 4]
        dists = [270, 150, 80, 160, 140, 95, 230, 130, 145, 155, 90, 240, 135, 120, 85, 140, 125, 150]
        for i in range(18):
            hole = Hole(
                course_id=course.id,
                hole_number=i + 1,
                par=pars[i],
                distance=dists[i],
                section=HoleSection.OUTWARD if i < 9 else HoleSection.INWARD,
                difficulty=(i % 18) + 1,
            )
            db.add(hole)
        db.commit()

    # 4. Création Parties
    game_draft = db.query(Game).filter_by(title="Tournoi d'Automne (Brouillon)").first()
    if not game_draft:
        print("Création des parties...")
        today = date.today()
        
        # Partie DRAFT
        g1 = Game(
            title="Tournoi d'Automne (Brouillon)",
            course_id=course.id,
            organizer_id=admin.id,
            start_date=today + timedelta(days=10),
            status=GameStatus.DRAFT,
        )
        # Partie OUVERTE
        g2 = Game(
            title="Open du Dimanche",
            course_id=course.id,
            organizer_id=admin.id,
            start_date=today + timedelta(days=2),
            status=GameStatus.REGISTRATION_OPEN,
        )
        # Partie EN COURS
        g3 = Game(
            title="Championnat Régional",
            course_id=course.id,
            organizer_id=admin.id,
            start_date=today,
            status=GameStatus.IN_PROGRESS,
            max_players=5,
            registered_count=3,
        )
        db.add_all([g1, g2, g3])
        db.commit()
        
        # Inscriptions pour G3
        db.refresh(g3)
        for i in range(3):
            gp = GamePlayer(
                game_id=g3.id,
                user_id=players[i].id,
                status=RegistrationStatus.PRESENT,
                attendance=AttendanceStatus.PRESENT
            )
            db.add(gp)
        db.commit()
        print("Seeding terminé avec succès !")
    else:
        print("La base de données contient déjà des données.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_db(db)
    finally:
        db.close()
