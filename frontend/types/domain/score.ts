export type ScoreStatus = "DRAFT" | "VALIDATED" | "DISPUTED";

export interface Score {
  id: string;
  game_id: string;
  player_id: string;
  hole_id: string;
  strokes: number;
  penalties: number;
  total_score: number;
  status: ScoreStatus;
  idempotency_key?: string;
  entered_at: string;
  updated_at?: string;
}

export interface ScoreCreate {
  hole_id: string;
  strokes: number;
  penalties: number;
  idempotency_key: string;
}

export interface ScoreUpdate {
  strokes?: number;
  penalties?: number;
  idempotency_key?: string;
}
