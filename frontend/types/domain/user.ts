export type UserRole = "ADMIN" | "PLAYER" | "MARKER";

export interface User {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  role: UserRole;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface TokenPayload {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface UserHistoryItem {
  game_id: string;
  title: string;
  course_name: string;
  start_date?: string;
  status: string;
  registered_at: string;
  attendance?: string;
  total_score?: number;
  relative_to_par?: number;
  position?: number;
}
