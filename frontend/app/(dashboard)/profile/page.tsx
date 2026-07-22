"use client";

import { useQuery } from "@tanstack/react-query";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { useAuth } from "@/components/auth/AuthContext";
import { userService } from "@/services/userService";
import { queryKeys } from "@/lib/queryKeys";
import { gameStatusLabels, getStatusBadgeClasses } from "@/lib/gameStatus";
import type { GameStatus } from "@/types/domain/game";
import { CalendarDays, MapPin, Trophy } from "lucide-react";

export default function ProfilePage() {
  const { user } = useAuth();

  const { data: history, isLoading } = useQuery({
    queryKey: ["users", user?.id, "history"],
    queryFn: () => userService.getUserHistory(user!.id),
    enabled: !!user,
  });

  return (
    <ProtectedRoute>
      <div className="space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Mon Profil</h1>
          <p className="mt-2 text-slate-600">Consultez vos informations et votre historique de parties.</p>
        </div>

        {user && (
          <div className="bg-white rounded-lg border shadow-sm p-6">
            <div className="flex items-center gap-4">
              <div className="h-16 w-16 bg-green-100 text-green-700 flex items-center justify-center rounded-full text-2xl font-bold">
                {user.first_name[0]}{user.last_name[0]}
              </div>
              <div>
                <h2 className="text-xl font-bold text-slate-900">{user.first_name} {user.last_name}</h2>
                <p className="text-slate-500">{user.email}</p>
                <div className="mt-2 inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ring-1 ring-inset bg-slate-50 text-slate-700 ring-slate-600/20">
                  Rôle: {user.role}
                </div>
              </div>
            </div>
          </div>
        )}

        <div>
          <h2 className="text-2xl font-bold text-slate-900 mb-4">Historique des parties</h2>
          
          <div className="bg-white rounded-lg border shadow-sm overflow-hidden">
            {isLoading ? (
              <div className="p-8 text-center text-slate-500">Chargement de l'historique...</div>
            ) : history && history.length > 0 ? (
              <ul className="divide-y divide-slate-200">
                {history.map((item) => (
                  <li key={item.game_id} className="p-4 sm:px-6 hover:bg-slate-50 transition-colors">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                      <div>
                        <div className="flex items-center gap-3 mb-1">
                          <h3 className="font-semibold text-slate-900">{item.title}</h3>
                          <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ring-1 ring-inset ${getStatusBadgeClasses(item.status as GameStatus)}`}>
                            {gameStatusLabels[item.status as GameStatus] || item.status}
                          </span>
                        </div>
                        <div className="flex flex-wrap gap-4 text-sm text-slate-500">
                          <span className="flex items-center">
                            <MapPin className="mr-1.5 h-4 w-4" />
                            {item.course_name}
                          </span>
                          <span className="flex items-center">
                            <CalendarDays className="mr-1.5 h-4 w-4" />
                            {item.start_date ? new Date(item.start_date).toLocaleDateString("fr-FR") : "Date non définie"}
                          </span>
                        </div>
                      </div>
                      
                      {item.status !== "CANCELLED" && (
                        <div className="flex items-center gap-4 bg-slate-50 px-4 py-2 rounded-md">
                          {item.total_score != null ? (
                            <div className="text-center">
                              <div className="text-xs text-slate-500 uppercase font-semibold">Score</div>
                              <div className="text-lg font-bold text-slate-900">{item.total_score}</div>
                            </div>
                          ) : null}
                          
                          {item.relative_to_par != null ? (
                            <div className="text-center">
                              <div className="text-xs text-slate-500 uppercase font-semibold">Par</div>
                              <div className={`text-lg font-bold ${item.relative_to_par! > 0 ? "text-red-600" : item.relative_to_par! < 0 ? "text-green-600" : "text-slate-600"}`}>
                                {item.relative_to_par! > 0 ? `+${item.relative_to_par}` : item.relative_to_par === 0 ? "E" : item.relative_to_par}
                              </div>
                            </div>
                          ) : null}

                          {item.position != null ? (
                            <div className="text-center pl-2 border-l border-slate-200">
                              <div className="text-xs text-slate-500 uppercase font-semibold">Pos</div>
                              <div className="text-lg font-bold text-amber-600 flex items-center justify-center">
                                {item.position === 1 && <Trophy className="w-4 h-4 mr-1" />}
                                #{item.position}
                              </div>
                            </div>
                          ) : null}
                        </div>
                      )}
                    </div>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="p-8 text-center text-slate-500">
                Vous n'avez participé à aucune partie pour le moment.
              </div>
            )}
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
