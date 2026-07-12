"use client";

import { useAuth } from "@/components/auth/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export function ProtectedRoute({
  children,
  adminOnly = false,
}: {
  children: React.ReactNode;
  adminOnly?: boolean;
}) {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !user) {
      router.push("/login");
    } else if (!isLoading && user && adminOnly && user.role !== "ADMIN") {
      router.push("/dashboard");
    }
  }, [user, isLoading, router, adminOnly]);

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-slate-200 border-t-green-600"></div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  if (adminOnly && user.role !== "ADMIN") {
    return null;
  }

  return <>{children}</>;
}
