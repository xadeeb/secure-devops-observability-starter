# Architecture

```mermaid
flowchart TD
    A[Developer push or pull request] --> B[GitHub Actions CI]
    B --> C[Install dependencies]
    C --> D[Pytest]
    D --> E[Build Docker image]
    A --> F[Security workflow]
    F --> G[pip-audit dependency scan]
    F --> H[Trivy image scan]
    E --> I[Local or future deployment target]
```

This starter intentionally separates CI and security checks from deployment. Add a deployment job only after choosing and documenting a safe target-specific authentication and runner design. For a public repository, do not run untrusted pull-request code on a privileged self-hosted runner.
