import { useQuery } from "@tanstack/react-query";
import { queryKeys } from "@/lib/queryKeys";
import { courseService } from "@/services/courseService";

export function useCourses() {
  return useQuery({
    queryKey: queryKeys.courses.all,
    queryFn: () => courseService.listCourses(),
  });
}

export function useCourse(id: string) {
  return useQuery({
    queryKey: queryKeys.courses.detail(id),
    queryFn: () => courseService.getCourse(id),
    enabled: !!id,
  });
}

export function useCourseHoles(id: string) {
  return useQuery({
    queryKey: queryKeys.courses.holes(id),
    queryFn: () => courseService.getCourseHoles(id),
    enabled: !!id,
  });
}
