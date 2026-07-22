import { api } from "@/lib/api";
import type { PaginatedData, ApiResponse } from "@/types/api";
import type { User, UserHistoryItem } from "@/types/domain/user";

export const userService = {
  getUsers: async (page = 1, size = 10) => {
    const res = await api.get<ApiResponse<PaginatedData<User>>>("/users", {
      params: { page, size },
    });
    return res.data.data;
  },

  getUser: async (id: string) => {
    const res = await api.get<ApiResponse<User>>(`/users/${id}`);
    return res.data.data;
  },

  getUserHistory: async (id: string) => {
    const res = await api.get<ApiResponse<UserHistoryItem[]>>(`/users/${id}/history`);
    return res.data.data;
  },
};
