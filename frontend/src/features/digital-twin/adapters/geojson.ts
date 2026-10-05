import { z } from "zod";

const positionSchema = z.array(z.number()).min(2);
const geometrySchema = z.object({
  type: z.enum(["Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon"]),
  coordinates: z.unknown(),
});

const featureSchema = z.object({
  type: z.literal("Feature"),
  id: z.union([z.string(), z.number()]).optional(),
  geometry: geometrySchema.nullable(),
  properties: z.record(z.unknown()).nullable().default({}),
});

const featureCollectionSchema = z.object({
  type: z.literal("FeatureCollection"),
  features: z.array(featureSchema),
});

export type GeoJsonFeatureCollection = z.infer<typeof featureCollectionSchema>;

export function parseFeatureCollection(value: unknown): GeoJsonFeatureCollection {
  return featureCollectionSchema.parse(value);
}

export function isValidPosition(value: unknown): boolean {
  return positionSchema.safeParse(value).success;
}
