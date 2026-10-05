import { describe, expect, it } from "vitest";
import { isValidPosition, parseFeatureCollection } from "./geojson";

describe("GeoJSON adapter", () => {
  it("accepts a valid feature collection", () => {
    const result = parseFeatureCollection({ type: "FeatureCollection", features: [] });
    expect(result.features).toHaveLength(0);
  });

  it("rejects unsupported payloads", () => {
    expect(() => parseFeatureCollection({ type: "FeatureCollection", features: [{ type: "bad" }] })).toThrow();
  });

  it("validates geographic positions", () => {
    expect(isValidPosition([12.1, 44.2])).toBe(true);
    expect(isValidPosition([12.1])).toBe(false);
  });
});
