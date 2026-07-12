"use client";

import { useState } from "react";
import { useAdminGames } from "@/hooks/queries/useGames";

import { Button } from "@/components/ui/button";
import { Plus, CalendarDays, Map, ShieldAlert } from "lucide-react";

export default function AdminGamesPage() {
  const [isCreating, setIsCreating] = useState(false);

  const { data: paginatedData, isLoading, error } = useAdminGames();
  const games = paginatedData?.items;

  return (
    <div className="space-y-6">
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
            {games?.map((game: any) => (
              <li key={game.id} className="p-4 sm:px-6 hover:bg-slate-50 transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex flex-col">
                    <p className="text-sm font-semibold text-slate-900">{game.title}</p>
                    <div className="mt-1 flex items-center gap-4 text-xs text-slate-500">
                      <span className="flex items-center">
                        <CalendarDays className="mr-1.5 h-4 w-4" />
                        {new Date(game.start_date).toLocaleDateString()}
                      </span>
                      <span className="flex items-center">
                        <Map className="mr-1.5 h-4 w-4" />
                        {game.course_name}
                      </span>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="inline-flex items-center rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-800">
                      {game.status}
                    </span>
                    <Button variant="outline" size="sm" className="hidden sm:inline-flex border-slate-200 text-slate-700">
                      Gérer
                    </Button>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
