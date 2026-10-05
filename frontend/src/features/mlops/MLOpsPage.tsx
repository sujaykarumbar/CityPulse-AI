import { useQuery } from "@tanstack/react-query";
import { Activity, Database, GitBranch, ShieldCheck } from "lucide-react";
import { api } from "../../lib/api/client";
import { z } from "zod";

const modelSchema = z.object({ model_id: z.string(), model_name: z.string(), model_version: z.string(), domain: z.string(), lifecycle: z.string(), validation_status: z.string(), deployment_status: z.string() });
const modelsSchema = z.array(modelSchema);

async function getModels() { const response = await api.get("/api/v1/mlops/models"); return modelsSchema.parse(response.data); }

export function MLOpsPage() {
  const models = useQuery({ queryKey: ["mlops-models"], queryFn: getModels });
  return <div className="mlops-page"><header className="mlops-header"><div><span className="panel-label">MODEL OPERATIONS</span><h1>MLOps control room</h1><p>Lifecycle, lineage, validation, and monitoring from measured registry data.</p></div><span className="data-badge simulated">LOCAL REGISTRY</span></header><section className="mlops-grid"><div className="mlops-summary"><div className="mlops-summary-card"><Database size={18} /><span>Registered models</span><strong>{models.data ? models.data.length : "N/A"}</strong></div><div className="mlops-summary-card"><ShieldCheck size={18} /><span>Promotion policy</span><strong>Validation required</strong></div><div className="mlops-summary-card"><Activity size={18} /><span>Monitoring</span><strong>Configured</strong></div></div><div className="mlops-panel"><div className="panel-heading"><div><span className="panel-label">MODEL REGISTRY</span><h2>Available records</h2></div><GitBranch size={18} /></div>{models.isLoading && <div className="mlops-empty">Loading registry...</div>}{models.isError && <div className="mlops-empty warning">Registry unavailable. No model state was inferred.</div>}{models.isSuccess && models.data.length === 0 && <div className="mlops-empty">No model records are registered in the current environment.</div>}{models.data && models.data.length > 0 && <div className="model-table">{models.data.map((model) => <div className="model-row" key={model.model_id}><strong>{model.model_name}</strong><span>{model.domain}</span><span>{model.model_version}</span><span>{model.lifecycle}</span><span>{model.validation_status}</span></div>)}</div>}</div><div className="mlops-note"><span className="panel-label">SCIENTIFIC STATUS</span><p>Model health, validation, drift, and predictive accuracy are separate concepts. Metrics are shown only when registered with a model record.</p></div></section></div>;
}
