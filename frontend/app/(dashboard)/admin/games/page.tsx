"use client";

import { useState } from "react";
import { useAdminGames } from "@/hooks/queries/useGames";
import { useCourses } from "@/hooks/queries/useCourses";
import { gameService } from "@/services/gameService";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Plus, CalendarDays, Map, ShieldAlert, X, Play, CheckCircle, DoorOpen, Users } from "lucide-react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { gameStatusLabels, getStatusBadgeClasses } from "@/lib/gameStatus";
import type { GameStatus } from "@/types/domain/game";
import Link from "next/link";

export default function AdminGamesPage() {
  const [isCreating, setIsCreating] = useState(false);
  const [formData, setFormData] = useState({
    title: "",
    course_id: "",
    start_date: "",
    max_players: 5,
  });
  const [formError, setFormError] = useState<string | null>(null);
  const [globalError, setGlobalError] = useState<string | null>(null);

  const queryClient = useQueryClient();
  const { data: paginatedData, isLoading, error } = useAdminGames();
  const games = paginatedData?.items;

  const { data: coursesData } = useCourses();
  const courses = coursesData?.items;

  const createMutation = useMutation({
    mutationFn: () => gameService.createGame(formData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "games"] });
      setIsCreating(false);
      setFormData({ title: "", course_id: "", start_date: "", max_players: 5 });
      setFormError(null);
    },
    onError: (err: any) => {
      setFormError(err?.message || "Erreur lors de la création de la partie");
    },
  });

  const statusMutation = useMutation({
    mutationFn: async ({ gameId, action }: { gameId: string; action: string }) => {
      setGlobalError(null);
      switch (action) {
        case "open-registration":
          return gameService.openRegistration(gameId);
        case "start":
          return gameService.startGame(gameId);
        case "finish":
          return gameService.finishGame(gameId);
        default:
          throw new Error("Action inconnue");
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin", "games"] });
    },
    onError: (err: any) => {
      setGlobalError(err?.message || "Erreur lors de la modification du statut.");
    },
  });

  const getAvailableActions = (status: GameStatus) => {
    switch (status) {
      case "DRAFT":
        return [{ action: "open-registration", label: "Ouvrir inscriptions", icon: DoorOpen, color: "text-green-600" }];
      case "REGISTRATION_OPEN":
      case "FULL":
      case "REGISTRATION_CLOSED":
        return [{ action: "start", label: "Démarrer", icon: Play, color: "text-blue-600" }];
      case "IN_PROGRESS":
        return [{ action: "finish", label: "Terminer", icon: CheckCircle, color: "text-purple-600" }];
      default:
        return [];
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.title || !formData.course_id || !formData.start_date) {
      setFormError("Veuillez remplir tous les champs obligatoires");
      return;
    }
    createMutation.mutate();
  };

  return (
    <ProtectedRoute adminOnly>
      <div className="space-y-6">
        {globalError && (
          <div className="relative rounded-lg border border-red-200 bg-red-50 p-4 shadow-sm">
            <div className="flex items-start">
              <ShieldAlert className="h-5 w-5 text-red-600 mt-0.5" />
              <div className="ml-3 flex-1">
                <h3 className="text-sm font-semibold text-red-800">Action impossible</h3>
                <p className="mt-1 text-sm text-red-700">{globalError}</p>
              </div>
              <button
                onClick={() => setGlobalError(null)}
                className="ml-auto inline-flex text-red-500 hover:text-red-700 focus:outline-none"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
          </div>
        )}

        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Gestion des Parties
          </h1>
          <Button 
            onClick={() => setIsCreating(true)}
            className="bg-green-600 hover:bg-green-700"
          >
            <Plus className="mr-2 h-5 w-5" />
            Nouvelle Partie
          </Button>
        </div>

        {/* Create Game Modal */}
        {isCreating && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
            <div className="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden">
              <div className="flex items-center justify-between p-6 border-b border-slate-200">
                <h2 className="text-lg font-bold text-slate-900">Nouvelle Partie</h2>
                <button
                  onClick={() => { setIsCreating(false); setFormError(null); }}
                  className="p-1 rounded-md text-slate-400 hover:text-slate-600"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
              <form onSubmit={handleSubmit} className="p-6 space-y-4">
                <div>
                  <Label htmlFor="title">Titre de la partie *</Label>
                  <Input
                    id="title"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    placeholder="Ex: Tournoi du printemps"
                    className="mt-1"
                  />
                </div>
                <div>
                  <Label htmlFor="course_id">Parcours *</Label>
                  <select
                    id="course_id"
                    value={formData.course_id}
                    onChange={(e) => setFormData({ ...formData, course_id: e.target.value })}
                    className="mt-1 block w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm shadow-sm focus:border-green-500 focus:outline-none focus:ring-1 focus:ring-green-500"
                  >
                    <option value="">Sélectionner un parcours</option>
                    {courses?.map((course: any) => (
                      <option key={course.id} value={course.id}>
                        {course.name}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <Label htmlFor="start_date">Date de début *</Label>
                  <Input
                    id="start_date"
                    type="date"
                    value={formData.start_date}
                    onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                    className="mt-1"
                  />
                </div>
                <div>
                  <Label htmlFor="max_players">Nombre max de joueurs (1-5)</Label>
                  <Input
                    id="max_players"
                    type="number"
                    min={1}
                    max={5}
                    value={formData.max_players}
                    onChange={(e) => setFormData({ ...formData, max_players: parseInt(e.target.value) || 5 })}
                    className="mt-1"
                  />
                </div>

                {formError && (
                  <div className="p-3 rounded-md bg-red-50 text-sm text-red-800 border border-red-200">
                    {formError}
                  </div>
                )}

                <div className="flex gap-3 pt-2">
                  <Button
                    type="button"
                    variant="outline"
                    className="flex-1"
                    onClick={() => { setIsCreating(false); setFormError(null); }}
                  >
                    Annuler
                  </Button>
                  <Button
                    type="submit"
                    className="flex-1 bg-green-600 hover:bg-green-700"
                    disabled={createMutation.isPending}
                  >
                    {createMutation.isPending ? "Création..." : "Créer la partie"}
                  </Button>
                </div>
              </form>
            </div>
          </div>
        )}

        {isLoading ? (
          <div className="flex justify-center py-12">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-slate-200 border-t-green-600"></div>
          </div>
        ) : error ? (
          <div className="rounded-lg border border-yellow-200 bg-yellow-50 p-6 text-center">
            <ShieldAlert className="mx-auto h-12 w-12 text-yellow-400" />
            <h3 className="mt-2 text-sm font-semibold text-yellow-800">Section Admin Indisponible</h3>
            <p className="mt-1 text-sm text-yellow-600">
              L'API d'administration n'est pas encore implémentée côté serveur.
            </p>
          </div>
        ) : (
          <div className="bg-white shadow-sm rounded-xl border border-slate-200 overflow-hidden">
            <ul className="divide-y divide-slate-200">
              {games?.length === 0 && (
                <li className="p-8 text-center text-sm text-slate-500">
                  Aucune partie créée. Cliquez sur "Nouvelle Partie" pour commencer.
                </li>
              )}
              {games?.map((game: any) => {
                const actions = getAvailableActions(game.status as GameStatus);
                return (
                  <li key={game.id} className="p-4 sm:px-6 hover:bg-slate-50 transition-colors">
                    <div className="flex items-center justify-between">
                      <div className="flex flex-col">
                        <p className="text-sm font-semibold text-slate-900">{game.title}</p>
                        <div className="mt-1 flex items-center gap-4 text-xs text-slate-500">
                          <span className="flex items-center">
                            <CalendarDays className="mr-1.5 h-4 w-4" />
                            {new Date(game.start_date).toLocaleDateString("fr-FR")}
                          </span>
                          <span className="flex items-center">
                            <Map className="mr-1.5 h-4 w-4" />
                            {game.course_name}
                          </span>
                          <span className="flex items-center">
                            <Users className="mr-1.5 h-4 w-4" />
                            {game.registered_count}/{game.max_players}
                          </span>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ring-1 ring-inset ${getStatusBadgeClasses(game.status as GameStatus)}`}>
                          {gameStatusLabels[game.status as GameStatus] || game.status}
                        </span>
                        {actions.map((act) => {
                          const Icon = act.icon;
                          return (
                            <Button
                              key={act.action}
                              variant="outline"
                              size="sm"
                              className={`hidden sm:inline-flex border-slate-200 ${act.color}`}
                              onClick={() => statusMutation.mutate({ gameId: game.id, action: act.action })}
                              disabled={statusMutation.isPending}
                            >
                              <Icon className="mr-1.5 h-4 w-4" />
                              {act.label}
                            </Button>
                          );
                        })}
                        <Link href={`/games/${game.id}/join`}>
                          <Button variant="outline" size="sm" className="hidden sm:inline-flex border-slate-200 text-slate-700">
                            Détails
                          </Button>
                        </Link>
                      </div>
                    </div>
                  </li>
                );
              })}
            </ul>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
