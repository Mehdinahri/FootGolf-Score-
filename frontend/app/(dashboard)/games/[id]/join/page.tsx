"use client";

import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useAuth } from "@/components/auth/AuthContext";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Calendar, MapPin, Users, ArrowLeft, Trophy } from "lucide-react";
import Link from "next/link";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { gameStatusLabels, getStatusBadgeClasses } from "@/lib/gameStatus";
import type { GameStatus } from "@/types/domain/game";

export default function GameJoinPage() {
  const { id } = useParams() as { id: string };
  const { user } = useAuth();
  const router = useRouter();
  const queryClient = useQueryClient();
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const { data: game, isLoading } = useQuery({
    queryKey: ["games", id],
    queryFn: async () => {
      const res = await api.get(`/games/${id}`);
      return res.data.data;
    },
  });

  const { data: players } = useQuery({
    queryKey: ["games", id, "players"],
    queryFn: async () => {
      const res = await api.get(`/games/${id}/players`);
      return res.data.data;
    },
  });

  const isRegistered = players?.some((p: any) => p.user_id === user?.id && p.status !== "CANCELLED");

  const registerMutation = useMutation({
    mutationFn: async () => {
      await api.post(`/games/${id}/register`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["games", id] });
      queryClient.invalidateQueries({ queryKey: ["games", id, "players"] });
    },
    onError: (error: any) => {
      setErrorMsg(error?.response?.data?.message || "Erreur lors de l'inscription");
    }
  });

  const cancelMutation = useMutation({
    mutationFn: async () => {
      await api.delete(`/games/${id}/registration`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["games", id] });
      queryClient.invalidateQueries({ queryKey: ["games", id, "players"] });
    },
    onError: (error: any) => {
      setErrorMsg(error?.response?.data?.message || "Erreur lors de l'annulation");
    }
  });

  if (isLoading) {
    return (
      <div className="flex justify-center py-12">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-slate-200 border-t-green-600"></div>
      </div>
    );
  }

  if (!game) {
    return (
      <div className="text-center py-12">
        <h2 className="text-xl font-bold text-slate-900">Partie introuvable</h2>
        <Link href="/dashboard" className="text-green-600 hover:underline mt-4 inline-block">Retour au tableau de bord</Link>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <Link href="/dashboard" className="inline-flex items-center text-sm text-slate-500 hover:text-slate-900">
        <ArrowLeft className="mr-2 h-4 w-4" />
        Retour au tableau de bord
      </Link>

      <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm">
        <div className="p-6 sm:p-8">
          <div className="flex justify-between items-start mb-6">
            <div>
              <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ring-1 ring-inset mb-3 ${getStatusBadgeClasses(game.status as GameStatus)}`}>
                {gameStatusLabels[game.status as GameStatus] || game.status}
              </span>
              <h1 className="text-3xl font-bold text-slate-900">{game.title}</h1>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-8">
            <div className="flex items-center text-slate-700">
              <Calendar className="h-5 w-5 mr-3 text-slate-400" />
              <div>
                <p className="text-sm font-medium">Date de début</p>
                <p className="text-sm text-slate-500">{new Date(game.start_date).toLocaleDateString("fr-FR")}</p>
              </div>
            </div>
            
            <div className="flex items-center text-slate-700">
              <MapPin className="h-5 w-5 mr-3 text-slate-400" />
              <div>
                <p className="text-sm font-medium">Lieu</p>
                <p className="text-sm text-slate-500">{game.course_name || "Parcours standard"}</p>
              </div>
            </div>

            <div className="flex items-center text-slate-700">
              <Users className="h-5 w-5 mr-3 text-slate-400" />
              <div>
                <p className="text-sm font-medium">Joueurs</p>
                <p className="text-sm text-slate-500">{game.registered_count} / {game.max_players} inscrits</p>
              </div>
            </div>
          </div>

          {errorMsg && (
            <div className="mb-6 p-4 rounded-md bg-red-50 text-sm text-red-800 border border-red-200">
              {errorMsg}
            </div>
          )}

          <div className="pt-6 border-t border-slate-100 flex flex-col sm:flex-row gap-4 justify-between items-center">
            {isRegistered ? (
              <>
                <p className="text-sm font-medium text-green-600 bg-green-50 px-4 py-2 rounded-lg">
                  Vous êtes inscrit à cette partie
                </p>
                <div className="flex gap-3 w-full sm:w-auto">
                  {(game.status === "REGISTRATION_OPEN" || game.status === "FULL") && (
                    <Button 
                      variant="outline" 
                      className="w-full sm:w-auto border-red-200 text-red-600 hover:bg-red-50"
                      onClick={() => cancelMutation.mutate()}
                      disabled={cancelMutation.isPending}
                    >
                      {cancelMutation.isPending ? "Annulation..." : "Annuler l'inscription"}
                    </Button>
                  )}
                  {game.status === "IN_PROGRESS" && (
                    <Button 
                      className="w-full sm:w-auto bg-green-600 hover:bg-green-700 text-white"
                      onClick={() => router.push(`/games/${id}/scorecard`)}
                    >
                      Ma Carte de Score
                    </Button>
                  )}
                </div>
              </>
            ) : (
              <Button 
                className="w-full sm:w-auto bg-slate-900 text-white hover:bg-slate-800 px-8"
                onClick={() => registerMutation.mutate()}
                disabled={registerMutation.isPending || game.registered_count >= game.max_players || game.status !== 'REGISTRATION_OPEN'}
              >
                {registerMutation.isPending ? "Inscription en cours..." : "S'inscrire à la partie"}
              </Button>
            )}
          </div>

          {/* Leaderboard link - visible when game is in progress or finished */}
          {(game.status === "IN_PROGRESS" || game.status === "FINISHED") && (
            <div className="mt-6 pt-4 border-t border-slate-100">
              <Link href={`/games/${id}/leaderboard`}>
                <Button 
                  variant="outline"
                  className="w-full sm:w-auto border-yellow-200 text-yellow-700 hover:bg-yellow-50"
                >
                  <Trophy className="mr-2 h-4 w-4" />
                  Voir le classement en direct
                </Button>
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
