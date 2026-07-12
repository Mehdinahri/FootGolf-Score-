import { api } from "@/lib/api";
import type { ApiResponse } from "@/types/api";
import type { GamePlayer, GamePlayerCreate } from "@/types/domain/gamePlayer";

export const registrationService = {
  async listPlayers(gameId: string) {
    const { data } = await api.get<ApiResponse<GamePlayer[]>>(`/games/${gameId}/players`);
    return data.data;
  },

  async register(gameId: string) {
    const { data } = await api.post<ApiResponse<GamePlayer>>(`/games/${gameId}/players`);
    return data.data;
  },

  async cancelRegistration(gameId: string) {
    const { data } = await api.delete<ApiResponse<null>>(`/games/${gameId}/players/me`);
    return data.data;
  },

  async addPlayerByAdmin(gameId: string, payload: GamePlayerCreate) {
    const { data } = await api.post<ApiResponse<GamePlayer>>(`/games/${gameId}/admin/players`, payload);
    return data.data;
  },

  async removePlayerByAdmin(gameId: string, playerId: string) {
    const { data } = await api.delete<ApiResponse<null>>(`/games/${gameId}/admin/players/${playerId}`);
    return data.data;
  },
};
