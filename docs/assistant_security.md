# Assistant Security

- No LLM API key is sent to the frontend.
- No arbitrary SQL, Python, or JavaScript execution is supported.
- Tools are allow-listed and permissioned.
- Tool errors are not converted into factual answers.
- Provider configuration is environment-based and unavailable by default.
- Conversation content should be retained only when a persistence layer is explicitly added.
