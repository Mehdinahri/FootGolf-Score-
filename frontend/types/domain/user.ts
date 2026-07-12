export type UserRole = "ADMIN" | "PLAYER";

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
