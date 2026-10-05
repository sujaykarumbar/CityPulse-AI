import { z } from "zod";

export const healthSchema = z.object({
  status: z.string(),
  environment: z.string(),
});

export const systemSchema = z.object({
  name: z.string(),
  version: z.string(),
  environment: z.string(),
});

export type Health = z.infer<typeof healthSchema>;
export type SystemInfo = z.infer<typeof systemSchema>;
export type ContractState = "verified" | "unavailable" | "unknown";
