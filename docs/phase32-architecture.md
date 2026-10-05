# Phase 32 Architecture

## Overview

Phase 32 extends CITYPULSE into a multi-city, interconnected systems intelligence layer. The design preserves the existing evidence-first architecture and adds a graph-backed regional intelligence layer rather than replacing earlier city-level modules.

## Core pattern

- Cities remain first-class nodes.
- Intercity relationships are modeled as explicit edges with provenance and uncertainty.
- Network metrics are informational and model-derived, never treated as ground truth infrastructure facts.
- Shock and cascade analysis are simulation workflows that remain labeled as modeled output.
- Regional strategy analysis is framed as decision support for human review.

## Components

### Urban network model

The system uses a directed urban graph with optional undirected views for centrality and structural analysis. Each edge preserves metadata for source, confidence, provenance, and relationship type.

### Registry and graph construction

The network registry stores network metadata and version information. The graph layer stores nodes, edges, and city-level profiles that remain distinguishable by layer (mobility, energy, economic, social).

### Dependency and centrality

Dependency indicators and centrality values are computed from the modeled graph. They are explicit network diagnostics rather than statements about real-world dependence or criticality.

### Cascade and resilience

Shock simulations use a bounded propagation process with depth and scenario labels. Network resilience evaluates connectivity and redundancy from graph structure, again without claiming physical system robustness.

### Policy coordination and foresight

Multi-city policy experiments compare local and regional outcomes, preserving trade-offs and uncertainty. Scenario outputs remain classified as MODEL_DERIVED or SCENARIO_ESTIMATE.

## Boundaries

- No live regional data platform is assumed.
- No autonomous regional interventions are executed.
- No network claim is treated as causal unless the evidence and assumptions support it.
