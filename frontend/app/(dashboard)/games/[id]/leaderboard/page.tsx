"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { useLeaderboard } from "@/hooks/queries/useLeaderboard";
import { useWebSocket } from "@/hooks/useWebSocket";
import type { LeaderboardRow } from "@/types/domain/leaderboard";
import { Trophy, Activity, Wifi, WifiOff } from "lucide-react";
import { cn } from "@/lib/utils";

export default function LeaderboardPage() {
  const { id } = useParams() as { id: string };
  const [leaderboard, setLeaderboard] = useState<LeaderboardRow[]>([]);
  
  const { isConnected, lastMessage } = useWebSocket(id);

  const { data: initialData, isLoading, error } = useLeaderboard(id);

  useEffect(() => {
    if (initialData?.rows) {
      setLeaderboard(initialData.rows);
    }
  }, [initialData]);

  useEffect(() => {
    if (lastMessage?.type === "LEADERBOARD_UPDATE") {
      setLeaderboard(lastMessage.payload.rows);
    }
  }, [lastMessage]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 flex items-center gap-2">
          <Trophy className="h-6 w-6 text-yellow-500" />
          Classement en direct
        </h1>
        <div className="flex items-center gap-2 text-sm">
          {isConnected ? (
            <span className="flex items-center text-green-600 bg-green-50 px-2.5 py-1 rounded-full font-medium">
              <Wifi className="mr-1.5 h-4 w-4" />
              En direct
            </span>
          ) : (
            <span className="flex items-center text-slate-500 bg-slate-100 px-2.5 py-1 rounded-full font-medium">
              <WifiOff className="mr-1.5 h-4 w-4" />
              Hors ligne
            </span>
          )}
        </div>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-12">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-slate-200 border-t-green-600"></div>
        </div>
      ) : error ? (
        <div className="rounded-lg border border-yellow-200 bg-yellow-50 p-6 text-center">
          <Activity className="mx-auto h-12 w-12 text-yellow-400" />
          <h3 className="mt-2 text-sm font-semibold text-yellow-800">Classement Indisponible</h3>
          <p className="mt-1 text-sm text-yellow-600">
            L'API du classement n'est pas encore implémentée côté serveur.
          </p>
        </div>
      ) : (
        <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200">
              <thead className="bg-slate-50">
                <tr>
                  <th scope="col" className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider w-16">
                    Pos
                  </th>
                  <th scope="col" className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    Joueur
                  </th>
                  <th scope="col" className="px-6 py-4 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    Trous
                  </th>
                  <th scope="col" className="px-6 py-4 text-center text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    Score
                  </th>
                  <th scope="col" className="px-6 py-4 text-right text-xs font-semibold text-slate-500 uppercase tracking-wider">
                    Total
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 bg-white">
                {leaderboard.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-6 py-8 text-center text-sm text-slate-500">
                      Aucun score enregistré pour le moment.
                    </td>
                  </tr>
                ) : (
                  leaderboard.map((row, idx) => (
                    <tr key={row.player_id} className={cn(idx % 2 === 0 ? "bg-white" : "bg-slate-50/50", "hover:bg-slate-50 transition-colors")}>
                      <td className="whitespace-nowrap px-6 py-4 text-sm font-bold text-slate-900">
                        {row.position}
                      </td>
                      <td className="whitespace-nowrap px-6 py-4 text-sm font-medium text-slate-900">
                        {row.first_name} {row.last_name}
                      </td>
                      <td className="whitespace-nowrap px-6 py-4 text-sm text-center text-slate-500">
                        {row.holes_completed}/18
                      </td>
                      <td className="whitespace-nowrap px-6 py-4 text-sm font-bold text-center">
                        <span className={cn(
                          "px-2 py-1 rounded-md",
                          row.relative_to_par < 0 ? "text-red-600 bg-red-50" : 
                          row.relative_to_par > 0 ? "text-blue-600 bg-blue-50" : 
                          "text-slate-600 bg-slate-100"
                        )}>
                          {row.relative_to_par > 0 ? "+" : ""}{row.relative_to_par === 0 ? "E" : row.relative_to_par}
                        </span>
                      </td>
                      <td className="whitespace-nowrap px-6 py-4 text-sm font-bold text-right text-slate-900">
                        {row.total_score}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
