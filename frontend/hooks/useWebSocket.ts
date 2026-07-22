"use client";

import { useEffect, useRef, useState } from "react";
import { useAuth } from "@/components/auth/AuthContext";
import { env } from "@/lib/env";

type WebSocketMessage = {
  type: string;
  data: any;
};

export function useWebSocket(gameId: string) {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const ws = useRef<WebSocket | null>(null);
  const { user } = useAuth();

  useEffect(() => {
    if (!user || !gameId) return;

    const wsUrl = `${env.NEXT_PUBLIC_WS_URL}/ws/games/${gameId}/leaderboard?token=${localStorage.getItem("access_token")}`;
    ws.current = new WebSocket(wsUrl);

    ws.current.onopen = () => {
      setIsConnected(true);
      console.log("WS Connected");
    };

    ws.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setLastMessage(data);
      } catch (e) {
        console.error("Erreur parsing WS message", e);
      }
    };

    ws.current.onclose = () => {
      setIsConnected(false);
      console.log("WS Disconnected");
    };

    return () => {
      ws.current?.close();
    };
  }, [gameId, user]);

  return { isConnected, lastMessage, ws: ws.current };
}
