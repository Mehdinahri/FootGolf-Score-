"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { useQuery } from "@tanstack/react-query";
import { queryClient } from "@/lib/queryClient";
import { api } from "@/lib/api";
import { queryKeys } from "@/lib/queryKeys";
import type { User } from "@/types/domain/user";
import type { ApiResponse } from "@/types/api";

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (access: string, refresh: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isInitialized, setIsInitialized] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      setIsAuthenticated(true);
    }
    setIsInitialized(true);
  }, []);

  const { data: user, isLoading: isQueryLoading, refetch } = useQuery({
    queryKey: queryKeys.auth.me,
    queryFn: async () => {
      const { data } = await api.get<ApiResponse<User>>("/auth/me");
      return data.data;
    },
    enabled: isAuthenticated,
    retry: false,
  });

  const login = (access: string, refresh: string) => {
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
    setIsAuthenticated(true);
    refetch();
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setIsAuthenticated(false);
    queryClient.clear();
    window.location.href = "/login";
  };

  const isLoading = !isInitialized || (isAuthenticated && isQueryLoading);

  return (
    <AuthContext.Provider value={{ user: user || null, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
