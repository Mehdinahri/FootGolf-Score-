import { api } from "@/lib/api";
import type { ApiResponse, PaginatedResponse } from "@/types/api";
import type { Game, GameCreate, GameUpdate } from "@/types/domain/game";

export const gameService = {
  async listGames() {
    const { data } = await api.get<PaginatedResponse<Game>>("/games");
    return data.data;
  },

  async listAdminGames() {
    const { data } = await api.get<PaginatedResponse<Game>>("/games/admin");
    return data.data;
  },

  async getGame(id: string) {
    const { data } = await api.get<ApiResponse<Game>>(`/games/${id}`);
    return data.data;
  },

  async createGame(payload: GameCreate) {
    const { data } = await api.post<ApiResponse<Game>>("/games", payload);
    return data.data;
  },

  async updateGame(id: string, payload: GameUpdate) {
    const { data } = await api.put<ApiResponse<Game>>(`/games/${id}`, payload);
    return data.data;
  },

  async publishGame(id: string) {
    const { data } = await api.post<ApiResponse<Game>>(`/games/${id}/publish`);
    return data.data;
  },

  async startGame(id: string) {
    const { data } = await api.post<ApiResponse<Game>>(`/games/${id}/start`);
    return data.data;
  },

  async finishGame(id: string) {
    const { data } = await api.post<ApiResponse<Game>>(`/games/${id}/finish`);
    return data.data;
  },

  async cancelGame(id: string, reason?: string) {
    const { data } = await api.post<ApiResponse<Game>>(`/games/${id}/cancel`, { reason });
    return data.data;
  },
};
