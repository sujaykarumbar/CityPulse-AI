import { z } from "zod";

export const citationSchema = z.object({
  source_type: z.string(),
  source_id: z.string(),
  label: z.string(),
  endpoint: z.string().nullable().optional(),
  timestamp: z.string().nullable().optional(),
});

export const assistantResponseSchema = z.object({
  answer: z.string(),
  intent: z.string(),
  entities: z.array(z.object({ kind: z.string(), value: z.string(), confidence: z.number().nullable().optional() })),
  evidence: z.array(z.record(z.unknown())),
  citations: z.array(citationSchema),
  actions: z.array(z.record(z.unknown())),
  uncertainty: z.string().nullable().optional(),
  data_freshness: z.string().nullable().optional(),
  metadata: z.record(z.unknown()),
  status: z.enum(["completed", "unavailable", "clarification", "blocked"]),
});

export type AssistantResponse = z.infer<typeof assistantResponseSchema>;
