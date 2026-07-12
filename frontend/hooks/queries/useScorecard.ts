import { useQuery } from "@tanstack/react-query";
import { queryKeys } from "@/lib/queryKeys";
import { scoreService } from "@/services/scoreService";

export function useScorecard(gameId: string) {
  return useQuery({
    queryKey: queryKeys.games.scorecard(gameId),
    queryFn: () => scoreService.getScorecard(gameId),
    enabled: !!gameId,
  });
}
