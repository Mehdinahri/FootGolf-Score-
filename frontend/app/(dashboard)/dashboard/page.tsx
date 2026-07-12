"use client";


import { useGames } from "@/hooks/queries/useGames";
import { Button } from "@/components/ui/button";
import { Calendar, Users, MapPin, Trophy } from "lucide-react";
import Link from "next/link";

interface Game {
  id: string;
  title: string;
  start_date: string;
  status: "DRAFT" | "REGISTRATION_OPEN" | "REGISTRATION_CLOSED" | "IN_PROGRESS" | "FINISHED" | "CANCELLED";
  registered_count: number;
  max_players: number;
  course_name: string;
}

export default function DashboardPage() {
  const { data: paginatedData, isLoading, error } = useGames();
  const games = paginatedData?.items;

  return (
    <div className="space-y-6 px-4 sm:px-0">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">
          Parties Disponibles
        </h1>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-12">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-slate-200 border-t-green-600"></div>
        </div>
      ) : error ? (
        <div className="rounded-lg border border-yellow-200 bg-yellow-50 p-6 text-center">
          <Trophy className="mx-auto h-12 w-12 text-yellow-400" />
          <h3 className="mt-2 text-sm font-semibold text-yellow-800">API Non Disponible</h3>
          <p className="mt-1 text-sm text-yellow-600">
            L'API pour récupérer les parties n'est pas encore implémentée côté serveur.
          </p>
        </div>
      ) : games?.length === 0 ? (
        <div className="rounded-lg border border-slate-200 bg-white p-12 text-center">
          <Calendar className="mx-auto h-12 w-12 text-slate-400" />
          <h3 className="mt-2 text-sm font-semibold text-slate-900">Aucune partie</h3>
          <p className="mt-1 text-sm text-slate-500">
            Il n'y a pas de partie ouverte à l'inscription pour le moment.
          </p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {games?.map((game) => (
            <div
              key={game.id}
              className="relative flex flex-col overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm transition-all hover:shadow-md"
            >
              <div className="p-5">
                <div className="flex items-center justify-between mb-4">
                  <span className="inline-flex items-center rounded-full bg-green-50 px-2.5 py-0.5 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20">
                    {game.status}
                  </span>
                  <span className="text-sm text-slate-500">
                    {new Date(game.start_date).toLocaleDateString("fr-FR")}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-slate-900 mb-2">
                  {game.title}
                </h3>
                <div className="space-y-2 mt-4 text-sm text-slate-600">
                  <div className="flex items-center">
                    <MapPin className="mr-2 h-4 w-4 text-slate-400" />
                    {game.course_name}
                  </div>
                  <div className="flex items-center">
                    <Users className="mr-2 h-4 w-4 text-slate-400" />
                    {game.registered_count} / {game.max_players} joueurs
                  </div>
                </div>
              </div>
              <div className="bg-slate-50 p-4 mt-auto border-t border-slate-100">
                <Link href={`/games/${game.id}/join`} className="w-full">
                  <Button className="w-full bg-slate-900 text-white hover:bg-slate-800">
                    Voir les détails
                  </Button>
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
