export interface Course {
  id: string;
  name: string;
  description?: string;
  hole_count: number;
  par_total: number;
  distance_total: number;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface CourseCreate {
  name: string;
  description?: string;
  hole_count?: number;
}

export interface CourseUpdate {
  name?: string;
  description?: string;
  hole_count?: number;
  is_active?: boolean;
}
