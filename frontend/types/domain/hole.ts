export type HoleSection = "OUTWARD" | "INWARD";

export interface Hole {
  id: string;
  course_id: string;
  hole_number: number;
  par: number;
  distance?: number;
  section: HoleSection;
}

export interface HoleCreate {
  hole_number: number;
  par: number;
  distance?: number;
}

export interface HoleBulkCreate {
  holes: HoleCreate[];
}
