import Dexie, { type Table } from 'dexie';

export interface OfflineScore {
  id: string; // uuid local (temporaire si besoin ou on utilise idempotency_key comme ID)
  game_id: string;
  hole_id: string;
  strokes: number;
  penalties: number;
  comment?: string;
  idempotency_key: string;
  status: "pending" | "synced" | "error";
  created_at: string;
}

export class FootGolfDB extends Dexie {
  scores!: Table<OfflineScore>;

  constructor() {
    super('FootGolfDB');
    this.version(2).stores({
      scores: 'id, game_id, hole_id, idempotency_key, status',
    });
  }
}

export const db = new FootGolfDB();
