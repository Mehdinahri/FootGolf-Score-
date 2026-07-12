export interface SyncScorePayload {
  hole_id: string;
  strokes: number;
  penalties: number;
  idempotency_key: string;
}

export interface SyncRequest {
  game_id: string;
  scores: SyncScorePayload[];
}

export interface SyncResponseItem {
  idempotency_key: string;
  status: "success" | "error";
  error?: string;
}

export interface SyncResponse {
  results: SyncResponseItem[];
}
