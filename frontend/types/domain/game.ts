export type GameStatus = "DRAFT" | "REGISTRATION_OPEN" | "FULL" | "REGISTRATION_CLOSED" | "IN_PROGRESS" | "FINISHED" | "CANCELLED";

export interface Game {
  id: string;
  title: string;
  course_id: string;
  organizer_id: string;
  start_date?: string;
  status: GameStatus;
  max_players?: number;
  registered_count: number;
  course_name?: string;
  created_at: string;
  updated_at?: string;
}

export interface GameCreate {
  title: string;
  course_id: string;
  start_date?: string;
  max_players?: number;
}

export interface GameUpdate {
  title?: string;
  course_id?: string;
  start_date?: string;
  max_players?: number;
  status?: GameStatus;
}
