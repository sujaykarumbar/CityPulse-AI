import { api } from "./client";
import { healthSchema, systemSchema } from "../../types/api";

export async function getHealth() {
  const response = await api.get("/health");
  return healthSchema.parse(response.data);
}

export async function getSystemInfo() {
  const response = await api.get("/api/v1/system");
  return systemSchema.parse(response.data);
}
