import { api } from "@/lib/api";
import type { ApiResponse } from "@/types/api";

interface LoginCredentials {
  email: string;
  password?: string;
}

export const authService = {
  async login(credentials: LoginCredentials) {
    // Note: If you use OAuth2PasswordRequestForm backend, you must send x-www-form-urlencoded
    // But our backend uses JSON payload `LoginRequest`
    const { data } = await api.post<ApiResponse<{ access_token: string; refresh_token: string }>>("/auth/login", credentials);
    return data.data;
  },

  async logout(refreshToken: string) {
    const { data } = await api.post<ApiResponse<null>>("/auth/logout", { refresh_token: refreshToken });
    return data;
  },
};
