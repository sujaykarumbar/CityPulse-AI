# Grounded Assistant Architecture

The assistant is a controlled interface, not an unrestricted chatbot.

```mermaid
flowchart LR
    User --> API[Assistant API]
    API --> Intent[Intent and entity routing]
    Intent --> Registry[Permissioned tool registry]
    Registry --> Domain[Verified CITYPULSE services]
    Domain --> Evidence[Structured evidence]
    Evidence --> Answer[Validated answer]
```

The current checkout exposes only the verified health and system API. Domain tools are registered but return `unavailable` until their corresponding backend APIs exist. The assistant never substitutes fabricated values.
