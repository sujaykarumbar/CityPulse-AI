from __future__ import annotations

import argparse
import json
from pathlib import Path

from citypulse.economic.profiles import build_city_economic_profile
from citypulse.economic.shocks import simulate_economic_shock
from citypulse.economic.specialization import analyze_specialization


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the CITYPULSE economic intelligence demo layer.")
    parser.add_argument("--output", default="reports/economic/demo.json")
    args = parser.parse_args()

    profile = build_city_economic_profile(
        "city-a",
        {"employment": 1200.0, "industry_mix": {"manufacturing": 0.6, "retail": 0.2}, "economic_diversity": 0.7},
    )
    specialization = analyze_specialization(
        city_id="city-a",
        sector="manufacturing",
        share=0.6,
        reference_share=0.35,
        period="2025-Q1",
    )
    shock = simulate_economic_shock(
        city_id="city-a",
        shock_type="freight_disruption",
        magnitude=0.6,
        sectors=["manufacturing"],
        duration_days=14,
    )

    payload = {"profile": profile, "specialization": specialization, "shock": shock}
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Economic intelligence summary written to {out}")


if __name__ == "__main__":
    main()
