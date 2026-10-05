import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { TwinViewport } from "./TwinViewport";

describe("TwinViewport", () => {
  it("renders an accessible 3D viewport canvas", () => {
    render(<TwinViewport layers={{ terrain: true, buildings: true, roads: true, zones: false }} />);

    expect(screen.getByRole("img", { name: /interactive 3d city viewport/i })).toBeInTheDocument();
  });
});
