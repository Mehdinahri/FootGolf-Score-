import type { GameStatus } from "@/types/domain/game";

/**
 * Traduit les statuts de partie en labels français lisibles.
 */
export const gameStatusLabels: Record<GameStatus, string> = {
  DRAFT: "Brouillon",
  REGISTRATION_OPEN: "Inscriptions ouvertes",
  FULL: "Complet",
  REGISTRATION_CLOSED: "Inscriptions fermées",
  IN_PROGRESS: "En cours",
  FINISHED: "Terminée",
  CANCELLED: "Annulée",
};

/**
 * Retourne les classes CSS pour le badge de statut.
 */
export function getStatusBadgeClasses(status: GameStatus): string {
  switch (status) {
    case "REGISTRATION_OPEN":
      return "bg-green-50 text-green-700 ring-green-600/20";
    case "IN_PROGRESS":
      return "bg-blue-50 text-blue-700 ring-blue-600/20";
    case "FULL":
      return "bg-amber-50 text-amber-700 ring-amber-600/20";
    case "REGISTRATION_CLOSED":
      return "bg-slate-100 text-slate-700 ring-slate-600/20";
    case "FINISHED":
      return "bg-purple-50 text-purple-700 ring-purple-600/20";
    case "CANCELLED":
      return "bg-red-50 text-red-700 ring-red-600/20";
    case "DRAFT":
    default:
      return "bg-slate-100 text-slate-600 ring-slate-500/20";
  }
}
