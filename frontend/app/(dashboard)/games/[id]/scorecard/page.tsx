"use client";

import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { ChevronLeft, ChevronRight, Save, WifiOff, Loader2 } from "lucide-react";
import { useScorecard } from "@/hooks/queries/useScorecard";
import { scoreService } from "@/services/scoreService";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { queryKeys } from "@/lib/queryKeys";
import { useOfflineSync } from "@/hooks/useOfflineSync";
import { offlineSyncManager } from "@/services/offlineSyncManager";
import { v4 as uuidv4 } from "uuid"; // We will need to add uuid if not there, or use crypto.randomUUID()

export default function ScorecardPage() {
  const { id } = useParams() as { id: string };
  const router = useRouter();
  const queryClient = useQueryClient();
  const [currentHoleIndex, setCurrentHoleIndex] = useState(0);
  const [localStrokes, setLocalStrokes] = useState<Record<string, number>>({});
  const [localPenalties, setLocalPenalties] = useState<Record<string, number>>({});
  const { isOnline } = useOfflineSync();
  const isOffline = !isOnline;

  const { data: scorecard, isLoading, error } = useScorecard(id);

  const saveScoreMutation = useMutation({
    mutationFn: async ({ holeId, strokes, penalties }: { holeId: string, strokes: number, penalties: number }) => {
      return scoreService.saveScore(id, {
        hole_id: holeId,
        strokes,
        penalties,
        idempotency_key: crypto.randomUUID(),
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.games.scorecard(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.games.leaderboard(id) });
    }
  });

  if (isLoading) {
    return (
      <div className="flex h-[calc(100vh-4rem)] items-center justify-center bg-slate-50">
        <Loader2 className="h-8 w-8 animate-spin text-green-600" />
      </div>
    );
  }

  if (error || !scorecard) {
    return (
      <div className="flex h-[calc(100vh-4rem)] items-center justify-center bg-slate-50 p-4">
        <div className="text-center text-slate-500">
          Impossible de charger la carte de score.
        </div>
      </div>
    );
  }

  const holes = scorecard.holes;
  
  // En cas d'absence de trous
  if (holes.length === 0) {
    return (
      <div className="flex h-[calc(100vh-4rem)] items-center justify-center bg-slate-50 p-4">
        <div className="text-center text-slate-500">
          Aucun trou configuré pour ce parcours.
        </div>
      </div>
    );
  }

  const hole = holes[currentHoleIndex];
  
  // Utiliser les valeurs locales si modifiées, sinon celles du serveur, sinon le par
  const currentStrokes = localStrokes[hole.id] ?? hole.score?.strokes ?? hole.par;
  const currentPenalties = localPenalties[hole.id] ?? hole.score?.penalties ?? 0;

  const handleStrokesChange = (delta: number) => {
    setLocalStrokes((prev) => ({
      ...prev,
      [hole.id]: Math.max(1, currentStrokes + delta),
    }));
  };

  const handlePenaltiesChange = (delta: number) => {
    setLocalPenalties((prev) => ({
      ...prev,
      [hole.id]: Math.max(0, currentPenalties + delta),
    }));
  };

  const saveScore = async () => {
    try {
      if (isOffline) {
        // Mode hors ligne
        await offlineSyncManager.addScoreToSync(
          id,
          hole.id,
          currentStrokes,
          currentPenalties,
          crypto.randomUUID()
        );
        // On n'invalide pas, on passe au trou suivant
      } else {
        // En ligne
        await saveScoreMutation.mutateAsync({
          holeId: hole.id,
          strokes: currentStrokes,
          penalties: currentPenalties,
        });
      }
      
      if (currentHoleIndex < holes.length - 1) {
        setCurrentHoleIndex((p) => p + 1);
      } else {
        router.push(`/games/${id}/leaderboard`);
      }
    } catch (err: any) {
      if (err?.code === "NETWORK_ERROR" || err?.code === "TIMEOUT") {
        // Fallback en cas d'erreur réseau soudaine
        await offlineSyncManager.addScoreToSync(
          id,
          hole.id,
          currentStrokes,
          currentPenalties,
          crypto.randomUUID()
        );
        if (currentHoleIndex < holes.length - 1) {
          setCurrentHoleIndex((p) => p + 1);
        } else {
          router.push(`/games/${id}/leaderboard`);
        }
      } else {
        console.error("Erreur lors de l'enregistrement", err);
      }
    }
  };

  return (
    <div className="flex h-[calc(100vh-4rem)] flex-col bg-slate-50">
      {/* Header du trou */}
      <div className="bg-slate-900 px-4 py-6 text-white shadow-md">
        <div className="flex items-center justify-between">
          <button
            onClick={() => setCurrentHoleIndex((p) => Math.max(0, p - 1))}
            disabled={currentHoleIndex === 0}
            className="p-2 text-slate-400 disabled:opacity-30"
          >
            <ChevronLeft className="h-8 w-8" />
          </button>

          <div className="text-center">
            <h2 className="text-sm font-semibold uppercase tracking-widest text-slate-400">
              Trou
            </h2>
            <div className="text-5xl font-black">{hole.hole_number}</div>
            <div className="mt-1 flex gap-4 text-sm font-medium text-slate-300">
              <span>Par {hole.par}</span>
              <span>•</span>
              <span>{hole.distance || "-"}m</span>
            </div>
          </div>

          <button
            onClick={() => setCurrentHoleIndex((p) => Math.min(holes.length - 1, p + 1))}
            disabled={currentHoleIndex === holes.length - 1}
            className="p-2 text-slate-400 disabled:opacity-30"
          >
            <ChevronRight className="h-8 w-8" />
          </button>
        </div>
      </div>

      {/* Saisie */}
      <div className="flex-1 overflow-y-auto px-4 py-8">
        <div className="mx-auto max-w-sm space-y-8">
          
          {/* Coups (Strokes) */}
          <div className="rounded-2xl bg-white p-6 shadow-sm border border-slate-200">
            <h3 className="text-center text-lg font-bold text-slate-900">Coups joués</h3>
            <div className="mt-6 flex items-center justify-between">
              <button
                onClick={() => handleStrokesChange(-1)}
                className="flex h-16 w-16 items-center justify-center rounded-full bg-slate-100 text-3xl font-bold text-slate-700 active:bg-slate-200 transition-colors"
              >
                -
              </button>
              <div className="text-6xl font-black text-slate-900 w-24 text-center">
                {currentStrokes}
              </div>
              <button
                onClick={() => handleStrokesChange(1)}
                className="flex h-16 w-16 items-center justify-center rounded-full bg-slate-100 text-3xl font-bold text-slate-700 active:bg-slate-200 transition-colors"
              >
                +
              </button>
            </div>
          </div>

          {/* Pénalités */}
          <div className="rounded-2xl bg-white p-6 shadow-sm border border-slate-200">
            <h3 className="text-center text-lg font-bold text-slate-900">Pénalités</h3>
            <div className="mt-6 flex items-center justify-between">
              <button
                onClick={() => handlePenaltiesChange(-1)}
                className="flex h-14 w-14 items-center justify-center rounded-full bg-red-50 text-2xl font-bold text-red-600 active:bg-red-100 transition-colors"
              >
                -
              </button>
              <div className="text-4xl font-black text-red-600 w-20 text-center">
                {currentPenalties}
              </div>
              <button
                onClick={() => handlePenaltiesChange(1)}
                className="flex h-14 w-14 items-center justify-center rounded-full bg-red-50 text-2xl font-bold text-red-600 active:bg-red-100 transition-colors"
              >
                +
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Footer / Validation */}
      <div className="bg-white p-4 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]">
        <div className="mx-auto max-w-sm flex flex-col gap-3">
          {isOffline && (
            <div className="flex items-center justify-center gap-2 text-xs font-medium text-amber-600 bg-amber-50 py-2 rounded-lg">
              <WifiOff className="h-4 w-4" />
              Mode hors-ligne: score sauvegardé localement
            </div>
          )}
          <Button
            onClick={saveScore}
            disabled={saveScoreMutation.isPending}
            className="w-full h-16 text-lg font-bold bg-green-600 hover:bg-green-700 rounded-xl"
          >
            {saveScoreMutation.isPending ? (
              <Loader2 className="mr-2 h-6 w-6 animate-spin" />
            ) : (
              <Save className="mr-2 h-6 w-6" />
            )}
            Enregistrer le score
          </Button>
        </div>
      </div>
    </div>
  );
}

