export type ApiErrorItem = {
  field?: string;
  message: string;
};

export type ApiError = {
  status: number | null;
  code: string;
  message: string;
  fieldErrors?: Record<string, string>;
  details?: unknown;
};

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
  errors?: ApiErrorItem[] | null;
}

export interface PaginatedData<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface PaginatedResponse<T> extends ApiResponse<PaginatedData<T>> {}
