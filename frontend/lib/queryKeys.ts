export const queryKeys = {
  auth: {
    me: ["me"] as const,
  },
  courses: {
    all: ["courses"] as const,
    list: (filters?: Record<string, any>) => ["courses", "list", filters] as const,
    detail: (id: string) => ["courses", "detail", id] as const,
    holes: (id: string) => ["courses", id, "holes"] as const,
  },
  games: {
    all: ["games"] as const,
    list: (filters?: Record<string, any>) => ["games", "list", filters] as const,
    detail: (id: string) => ["games", "detail", id] as const,
    players: (id: string) => ["games", id, "players"] as const,
    scorecard: (id: string) => ["games", id, "scorecard"] as const,
    leaderboard: (id: string) => ["games", id, "leaderboard"] as const,
  },
};
