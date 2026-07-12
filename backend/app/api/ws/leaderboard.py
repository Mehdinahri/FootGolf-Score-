import uuid
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.api import deps
from app.repositories.game_repo import game_repo
from app.services.broadcast_service import broadcast_service
from app.services.leaderboard_service import LeaderboardService

router = APIRouter()

@router.websocket("/games/{game_id}/leaderboard")
async def websocket_leaderboard(websocket: WebSocket, game_id: uuid.UUID, db: Session = Depends(deps.get_db)):
    game_id_str = str(game_id)
    # Vérifier que la partie existe
    game = game_repo.get(db, id=game_id)
    if not game:
        await websocket.close(code=4004)
        return

    await broadcast_service.connect(game_id_str, websocket)
    try:
        # Envoyer l'état initial
        initial_data = LeaderboardService.get_leaderboard(db, game)
        from fastapi.encoders import jsonable_encoder
        import json
        await websocket.send_text(json.dumps({"type": "LEADERBOARD_UPDATE", "data": jsonable_encoder(initial_data)}))
        
        while True:
            # Garder la connexion ouverte
            data = await websocket.receive_text()
            # On ignore les messages entrants, c'est du broadcast descendnat
    except WebSocketDisconnect:
        broadcast_service.disconnect(game_id_str, websocket)
