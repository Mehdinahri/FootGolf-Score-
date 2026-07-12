import { useQuery } from "@tanstack/react-query";
import { queryKeys } from "@/lib/queryKeys";
import { leaderboardService } from "@/services/leaderboardService";

export function useLeaderboard(gameId: string) {
  return useQuery({
    queryKey: queryKeys.games.leaderboard(gameId),
    queryFn: () => leaderboardService.getLeaderboard(gameId),
    enabled: !!gameId,
  });
}
