import { test, expect } from 'vitest';
import { normalizeApiError } from "@/lib/api";

test('normalizeApiError handles 422 errors correctly', () => {
  const axiosError = {
    isAxiosError: true,
    response: {
      status: 422,
      data: {
        detail: [
          { loc: ["body", "email"], msg: "Invalid email" }
        ]
      }
    }
  };

  const result = normalizeApiError(axiosError);
  expect(result.status).toBe(422);
  expect(result.code).toBe("VALIDATION_ERROR");
  expect(result.fieldErrors?.email).toBe("Invalid email");
});
