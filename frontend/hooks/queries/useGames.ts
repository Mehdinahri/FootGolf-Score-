import { useQuery } from "@tanstack/react-query";
import { queryKeys } from "@/lib/queryKeys";
import { gameService } from "@/services/gameService";
import { registrationService } from "@/services/registrationService";

export function useGames() {
  return useQuery({
    queryKey: queryKeys.games.all,
    queryFn: () => gameService.listGames(),
  });
}

export function useAdminGames() {
  return useQuery({
    queryKey: ["admin", "games"],
    queryFn: () => gameService.listAdminGames(),
  });
}

export function useGame(id: string) {
  return useQuery({
    queryKey: queryKeys.games.detail(id),
    queryFn: () => gameService.getGame(id),
    enabled: !!id,
  });
}

export function useGamePlayers(gameId: string) {
  return useQuery({
    queryKey: queryKeys.games.players(gameId),
    queryFn: () => registrationService.listPlayers(gameId),
    enabled: !!gameId,
  });
}
