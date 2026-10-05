import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
  timeout: 5000,
  headers: { Accept: "application/json" },
});

export function requestId(error: unknown): string | undefined {
  if (axios.isAxiosError(error)) return error.response?.headers["x-request-id"];
  return undefined;
}
