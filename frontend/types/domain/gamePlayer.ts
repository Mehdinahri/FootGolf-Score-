import type { User } from "./user";

export type RegistrationStatus = "REGISTERED" | "CANCELLED" | "PLAYING" | "FINISHED" | "DNF";

export interface GamePlayer {
  game_id: string;
  user_id: string;
  status: RegistrationStatus;
  start_order?: number;
  registered_at: string;
  updated_at?: string;
  user?: User; // Depending on backend inclusion
}

export interface GamePlayerCreate {
  user_id: string;
  start_order?: number;
}
