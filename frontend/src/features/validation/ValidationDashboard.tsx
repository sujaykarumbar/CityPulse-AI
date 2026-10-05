import { useQuery } from "@tanstack/react-query";
import { Activity, AlertTriangle, ClipboardCheck, Database, FlaskConical } from "lucide-react";
import { z } from "zod";
import { api } from "../../lib/api/client";
import "./validation.css";

const statusSchema = z.object({
  status: z.string(),
  real_datasets: z.string(),
  trained_models: z.string(),
  validation_runs: z.number(),
  experiment_results: z.string(),
  limitations: z.array(z.string()),
});

const scorecardSchema = z.record(z.string(), z.unknown());
const metricSchema = z.object({
  name: z.string(),
  value: z.number().nullable(),
  status: z.string(),
  units: z.string().nullable().optional(),
});
const runSchema = z.object({
  validation_id: z.string(),
  task: z.string(),
  timestamp: z.string(),
  status: z.string(),
  result_type: z.string(),
  dataset_version: z.string().nullable().optional(),
  model_version: z.string().nullable().optional(),
  metric_results: z.array(metricSchema),
  limitations: z.array(z.string()),
});

async function getStatus() {
  const response = await api.get("/api/v1/validation/status");
  return statusSchema.parse(response.data);
}

async function getScorecard() {
  const response = await api.get("/api/v1/validation/scorecard");
  return scorecardSchema.parse(response.data);
}

async function getRuns() {
  const response = await api.get("/api/v1/validation/runs");
  return z.array(runSchema).parse(response.data);
}

function displayStatus(value: unknown) {
  if (typeof value !== "string") return "NOT_MEASURED";
  return value.replace(/_/g, " ");
}

export function ValidationDashboard() {
  const status = useQuery({ queryKey: ["validation-status"], queryFn: getStatus });
  const scorecard = useQuery({ queryKey: ["validation-scorecard"], queryFn: getScorecard });
  const runs = useQuery({ queryKey: ["validation-runs"], queryFn: getRuns });

  return (
    <main className="validation-page">
      <header className="validation-header">
        <div>
          <span className="panel-label">RESEARCH & EVIDENCE</span>
          <h1>Validation laboratory</h1>
          <p>Measured evidence for models, simulations, and robustness experiments.</p>
        </div>
        <span className="validation-status-tag"><Activity size={14} />{status.data?.status ?? (status.isError ? "SERVICE UNAVAILABLE" : "CHECKING STATUS")}</span>
      </header>

      {status.isError && <div className="validation-alert"><AlertTriangle size={16} />Validation service unavailable. No results are inferred.</div>}

      <section className="validation-overview" aria-label="Validation data availability">
        <div className="validation-overview-item"><Database size={17} /><span>Verified datasets</span><strong>{status.data?.real_datasets ?? "NOT_MEASURED"}</strong></div>
        <div className="validation-overview-item"><FlaskConical size={17} /><span>Trained models</span><strong>{status.data?.trained_models ?? "NOT_MEASURED"}</strong></div>
        <div className="validation-overview-item"><ClipboardCheck size={17} /><span>Stored validation runs</span><strong>{status.data?.validation_runs ?? "NOT_MEASURED"}</strong></div>
      </section>

      <section className="validation-panel">
        <div className="panel-heading"><div><span className="panel-label">VALIDATION SCORECARD</span><h2>Evidence by dimension</h2></div><span className="validation-caption">No aggregate score</span></div>
        {scorecard.isLoading && <p className="validation-empty">Loading scorecard...</p>}
        {scorecard.isError && <p className="validation-empty warning">Scorecard unavailable.</p>}
        {scorecard.data && <div className="scorecard-grid">{Object.entries(scorecard.data).map(([dimension, value]) => <div className="scorecard-item" key={dimension}><span>{dimension.replace(/_/g, " ")}</span><strong>{displayStatus(value)}</strong></div>)}</div>}
        {status.data && status.data.limitations.length > 0 && <div className="validation-limitation"><strong>Current limitation</strong><span>{status.data.limitations.join(" ")}</span></div>}
      </section>

      <section className="validation-panel">
        <div className="panel-heading"><div><span className="panel-label">RECORDED EXPERIMENTS</span><h2>Validation runs</h2></div><span className="validation-caption">Values shown only when measured</span></div>
        {runs.isLoading && <p className="validation-empty">Loading validation runs...</p>}
        {runs.isError && <p className="validation-empty warning">Validation runs unavailable.</p>}
        {runs.data?.length === 0 && <p className="validation-empty">No validation runs are registered. Model performance remains NOT_MEASURED.</p>}
        {runs.data && runs.data.length > 0 && <div className="validation-run-list">{runs.data.map((run) => <article className="validation-run" key={run.validation_id}>
          <div className="validation-run-heading"><div><strong>{run.task}</strong><span>{run.validation_id}</span></div><span className="validation-run-status">{displayStatus(run.status)}</span></div>
          <div className="validation-run-meta"><span>{run.result_type}</span><span>Dataset: {run.dataset_version ?? "NOT_RECORDED"}</span><span>Model: {run.model_version ?? "NOT_RECORDED"}</span><time dateTime={run.timestamp}>{new Date(run.timestamp).toLocaleString()}</time></div>
          {run.metric_results.length > 0 ? <div className="validation-metrics">{run.metric_results.map((metric) => <div key={metric.name}><span>{metric.name}</span><strong>{metric.value === null ? displayStatus(metric.status) : `${metric.value.toPrecision(4)}${metric.units ? ` ${metric.units}` : ""}`}</strong></div>)}</div> : <p className="validation-run-empty">NOT_MEASURED</p>}
          {run.limitations.length > 0 && <p className="validation-run-limitation">{run.limitations.join(" ")}</p>}
        </article>)}</div>}
      </section>
    </main>
  );
}