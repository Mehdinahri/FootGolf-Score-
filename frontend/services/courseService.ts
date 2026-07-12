import { api } from "@/lib/api";
import type { ApiResponse, PaginatedResponse } from "@/types/api";
import type { Course, CourseCreate, CourseUpdate } from "@/types/domain/course";
import type { Hole, HoleBulkCreate } from "@/types/domain/hole";

export const courseService = {
  async listCourses() {
    const { data } = await api.get<PaginatedResponse<Course>>("/courses");
    return data.data; // PaginatedData<Course>
  },

  async getCourse(id: string) {
    const { data } = await api.get<ApiResponse<Course>>(`/courses/${id}`);
    return data.data;
  },

  async createCourse(payload: CourseCreate) {
    const { data } = await api.post<ApiResponse<Course>>("/courses", payload);
    return data.data;
  },

  async updateCourse(id: string, payload: CourseUpdate) {
    const { data } = await api.put<ApiResponse<Course>>(`/courses/${id}`, payload);
    return data.data;
  },

  async getCourseHoles(courseId: string) {
    const { data } = await api.get<ApiResponse<Hole[]>>(`/courses/${courseId}/holes`);
    return data.data;
  },

  async bulkSaveHoles(courseId: string, payload: HoleBulkCreate) {
    const { data } = await api.post<ApiResponse<Hole[]>>(`/courses/${courseId}/holes/bulk`, payload);
    return data.data;
  },
};
