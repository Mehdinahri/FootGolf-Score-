import { api } from "@/lib/api";
import type { ApiResponse } from "@/types/api";
import type { Scorecard } from "@/types/domain/scorecard";
import type { ScoreCreate, ScoreUpdate, Score } from "@/types/domain/score";

export const scoreService = {
  async getScorecard(gameId: string) {
    const { data } = await api.get<ApiResponse<Scorecard>>(`/games/${gameId}/scorecard`);
    return data.data;
  },

  async saveScore(gameId: string, payload: ScoreCreate) {
    const { data } = await api.post<ApiResponse<Score>>(`/games/${gameId}/scores`, payload);
    return data.data;
  },

  async updateScore(gameId: string, scoreId: string, payload: ScoreUpdate) {
    const { data } = await api.put<ApiResponse<Score>>(`/games/${gameId}/scores/${scoreId}`, payload);
    return data.data;
  },

  async validateScore(gameId: string, scoreId: string) {
    const { data } = await api.post<ApiResponse<Score>>(`/games/${gameId}/scores/${scoreId}/validate`);
    return data.data;
  },
};
