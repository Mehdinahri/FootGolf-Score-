import type { HoleSection } from "./hole";
import type { ScoreStatus } from "./score";

export interface ScorecardGameDto {
  id: string;
  title: string;
  status: string;
}

export interface ScorecardCourseDto {
  id: string;
  name: string;
  total_par: number;
}

export interface ScorecardPlayerDto {
  id: string;
  first_name: string;
  last_name: string;
}

export interface ScorecardHoleScore {
  id: string;
  strokes: number;
  penalties: number;
  total: number;
  status: ScoreStatus;
}

export interface ScorecardHole {
  id: string;
  hole_number: number;
  par: number;
  distance: number | null;
  section: HoleSection;
  score: ScorecardHoleScore | null;
}

export interface ScorecardTotals {
  outward: number;
  return: number;
  total: number;
  relative_to_par: number;
}

export interface ScorecardProgress {
  completed_holes: number;
  current_hole: number;
  total_holes: number;
}

export interface Scorecard {
  game: ScorecardGameDto;
  course: ScorecardCourseDto;
  player: ScorecardPlayerDto;
  progress: ScorecardProgress;
  totals: ScorecardTotals;
  holes: ScorecardHole[];
}
