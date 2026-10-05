import { useMutation } from "@tanstack/react-query";
import { ArrowUp, Bot, CircleAlert, FileText, LoaderCircle, Sparkles } from "lucide-react";
import { FormEvent, useState } from "react";
import { sendAssistantMessage } from "../../lib/api/assistant";
import type { AssistantResponse } from "../../types/assistant";

const suggestions = ["What is happening with traffic right now?", "Which areas have unusual traffic conditions?", "What models are available?", "What happens if this road is closed?"];

export function AssistantPage() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState<AssistantResponse | null>(null);
  const mutation = useMutation({ mutationFn: (value: string) => sendAssistantMessage(value), onSuccess: setResponse });
  const submit = (event: FormEvent) => { event.preventDefault(); const value = message.trim(); if (value) { mutation.mutate(value); setMessage(""); } };

  return <div className="assistant-page">
    <header className="assistant-header"><div><span className="panel-label">GROUNDED ANALYTICS</span><h1>CITYPULSE assistant</h1><p>A controlled interface to verified CITYPULSE tools and evidence.</p></div><div className="assistant-state"><span className="status-dot offline" /> Domain tools unavailable</div></header>
    <main className="assistant-layout">
      <section className="assistant-chat" aria-label="CITYPULSE assistant chat">
        <div className="assistant-intro"><div className="assistant-icon"><Sparkles size={21} /></div><div><h2>Ask the city intelligence layer</h2><p>Questions are routed to registered backend tools. Unavailable data is reported directly.</p></div></div>
        {!response && <div className="suggestion-grid">{suggestions.map((item) => <button key={item} onClick={() => setMessage(item)}>{item}<ArrowUp size={13} /></button>)}</div>}
        {response && <div className={`assistant-response ${response.status}`}><div className="response-meta"><Bot size={16} /><span>{response.intent}</span><span className="response-status">{response.status}</span></div><p>{response.answer}</p>{response.uncertainty && <div className="assistant-notice"><CircleAlert size={14} /> {response.uncertainty}</div>}{response.citations.length > 0 && <div className="citation-list"><span className="panel-label">SOURCES</span>{response.citations.map((citation) => <button key={`${citation.source_type}-${citation.source_id}`}><FileText size={14} /> {citation.label}</button>)}</div>}</div>}
        {mutation.isError && <div className="assistant-error"><CircleAlert size={15} /> Unable to reach the assistant service. No answer was generated.</div>}
        <form className="assistant-composer" onSubmit={submit}><input value={message} onChange={(event) => setMessage(event.target.value)} placeholder="Ask CITYPULSE..." aria-label="Ask CITYPULSE" maxLength={4000} /><button disabled={!message.trim() || mutation.isPending} aria-label="Send question">{mutation.isPending ? <LoaderCircle className="spin" size={17} /> : <ArrowUp size={17} />}</button></form>
      </section>
      <aside className="assistant-context"><span className="panel-label">GROUNDING CONTRACT</span><h2>Evidence first</h2><p>The assistant does not access databases, models, or files directly. It can only use registered, permission-checked backend tools.</p><div className="contract-row"><span>Provider</span><strong>Not configured</strong></div><div className="contract-row"><span>Live traffic</span><strong>Unavailable</strong></div><div className="contract-row"><span>Risk events</span><strong>Unavailable</strong></div><div className="contract-row"><span>Simulation</span><strong>Unavailable</strong></div><div className="assistant-footnote">Observed data, forecasts, simulations, and decision analysis remain separate states.</div></aside>
    </main>
  </div>;
}
