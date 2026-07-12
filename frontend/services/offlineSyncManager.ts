import { db } from "@/lib/offlineDb";
import { api } from "@/lib/api";
import type { SyncRequest, SyncResponse } from "@/types/domain/offlineSync";

export const offlineSyncManager = {
  async addScoreToSync(game_id: string, hole_id: string, strokes: number, penalties: number, idempotency_key: string) {
    await db.scores.put({
      id: crypto.randomUUID(),
      game_id,
      hole_id,
      strokes,
      penalties,
      idempotency_key,
      status: "pending",
      created_at: new Date().toISOString(),
    });
  },

  async syncPendingScores() {
    if (!navigator.onLine) return;

    const pendingScores = await db.scores.where("status").equals("pending").toArray();
    if (pendingScores.length === 0) return;

    // Group by game_id
    const games = new Set(pendingScores.map(s => s.game_id));

    for (const gameId of games) {
      const scoresForGame = pendingScores.filter(s => s.game_id === gameId);
      
      const payload: SyncRequest = {
        game_id: gameId,
        scores: scoresForGame.map(s => ({
          hole_id: s.hole_id,
          strokes: s.strokes,
          penalties: s.penalties,
          idempotency_key: s.idempotency_key,
        })),
      };

      try {
        const { data } = await api.post<{ success: boolean; data: SyncResponse }>("/offline-sync/scores", payload);
        
        if (data.success && data.data.results) {
          for (const result of data.data.results) {
            const scoreInDb = await db.scores.where("idempotency_key").equals(result.idempotency_key).first();
            if (scoreInDb) {
              await db.scores.update(scoreInDb.id, {
                status: result.status === "success" ? "synced" : "error",
              });
            }
          }
        }
      } catch (err) {
        console.error("Erreur lors de la synchronisation du jeu", gameId, err);
      }
    }
  },
};
