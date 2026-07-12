import axios, { AxiosError } from "axios";
import { env } from "./env";
import type { ApiError, ApiResponse } from "@/types/api";

export const api = axios.create({
  baseURL: env.NEXT_PUBLIC_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 15000,
});

// Interceptor for attaching token
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Interceptor for handling 401 and refreshing token
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as any;
    
    if (error.response?.status === 401 && !originalRequest._retry && originalRequest.url !== "/auth/refresh") {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem("refresh_token");
        if (!refreshToken) throw new Error("No refresh token");

        const { data } = await axios.post<ApiResponse<{ access_token: string, refresh_token: string }>>(
          `${env.NEXT_PUBLIC_API_URL}/auth/refresh`,
          { refresh_token: refreshToken }
        );

        localStorage.setItem("access_token", data.data.access_token);
        localStorage.setItem("refresh_token", data.data.refresh_token);

        api.defaults.headers.common.Authorization = `Bearer ${data.data.access_token}`;
        originalRequest.headers.Authorization = `Bearer ${data.data.access_token}`;
        return api(originalRequest);
      } catch (err) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        if (typeof window !== "undefined" && window.location.pathname !== "/login") {
          window.location.href = "/login";
        }
        return Promise.reject(normalizeApiError(error));
      }
    }
    return Promise.reject(normalizeApiError(error));
  }
);

export function normalizeApiError(error: unknown): ApiError {
  if (axios.isAxiosError(error)) {
    const status = error.response?.status || null;
    const responseData = error.response?.data as ApiResponse<any> | undefined;

    // FastAPI 422 Validation Error
    if (status === 422) {
      const detail = (error.response?.data as any)?.detail;
      const fieldErrors: Record<string, string> = {};
      if (Array.isArray(detail)) {
        detail.forEach((err: any) => {
          const field = err.loc?.slice(-1)[0] || "unknown";
          fieldErrors[field] = err.msg;
        });
      }
      return {
        status,
        code: "VALIDATION_ERROR",
        message: "Erreur de validation des données",
        fieldErrors,
      };
    }

    // Known API Error
    if (responseData && !responseData.success) {
      const fieldErrors: Record<string, string> = {};
      if (responseData.errors) {
        responseData.errors.forEach(err => {
          if (err.field) fieldErrors[err.field] = err.message;
        });
      }
      return {
        status,
        code: status?.toString() || "UNKNOWN",
        message: responseData.message || "Erreur serveur",
        fieldErrors: Object.keys(fieldErrors).length > 0 ? fieldErrors : undefined,
      };
    }

    // Network / timeout
    if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
      return { status, code: "TIMEOUT", message: "Le serveur met trop de temps à répondre" };
    }
    if (!error.response) {
      return { status, code: "NETWORK_ERROR", message: "Problème de connexion réseau" };
    }

    return { status, code: "API_ERROR", message: error.message };
  }

  return { status: null, code: "UNKNOWN_ERROR", message: "Une erreur inattendue est survenue" };
}
