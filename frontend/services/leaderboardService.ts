import { api } from "@/lib/api";
import type { ApiResponse } from "@/types/api";
import type { Leaderboard } from "@/types/domain/leaderboard";

export const leaderboardService = {
  async getLeaderboard(gameId: string) {
    const { data } = await api.get<ApiResponse<Leaderboard>>(`/games/${gameId}/leaderboard`);
    return data.data;
  },
};
