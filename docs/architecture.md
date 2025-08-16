## ai-smartcloudops Architecture

This is an initial high-level architecture sketch. It will evolve as the project grows.

```mermaid
graph TD
    Dev[Developer / CLI] -->|runs| App[ai-smartcloudops (Python package)]
    App --> Core[Core Services]
    Core --> Integrations[Cloud Providers / Tooling]
    App --> API[Future REST API (optional)]
    API --> Clients[UI / Automation]
    Tests[pytest] --> App

    subgraph Runtime [Python 3.11]
        App
        Core
    end
```


