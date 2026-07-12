export interface LeaderboardRow {
  player_id: string;
  first_name: string;
  last_name: string;
  position: number;
  total_score: number;
  relative_to_par: number;
  holes_completed: number;
  is_dnf: boolean;
}

export interface Leaderboard {
  game_id: string;
  status: string;
  rows: LeaderboardRow[];
}
