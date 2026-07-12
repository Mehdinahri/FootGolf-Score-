"use client";

import { WifiOff } from "lucide-react";
import { useOfflineSync } from "@/hooks/useOfflineSync";

export function NetworkStatus() {
  const { isOnline } = useOfflineSync();

  if (isOnline) return null;

  return (
    <div className="bg-red-600 px-4 py-2 text-center text-sm font-medium text-white flex items-center justify-center gap-2">
      <WifiOff className="h-4 w-4" />
      Vous êtes hors-ligne. Les scores seront sauvegardés localement.
    </div>
  );
}
