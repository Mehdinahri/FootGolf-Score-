"use client";

import { useEffect, useState } from "react";
import { offlineSyncManager } from "@/services/offlineSyncManager";

export function useOfflineSync() {
  const [isOnline, setIsOnline] = useState(typeof window !== "undefined" ? navigator.onLine : true);

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      // Trigger sync when coming back online
      offlineSyncManager.syncPendingScores().catch(console.error);
    };

    const handleOffline = () => {
      setIsOnline(false);
    };

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    // Initial check
    if (navigator.onLine) {
      offlineSyncManager.syncPendingScores().catch(console.error);
    }

    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  return { isOnline };
}
