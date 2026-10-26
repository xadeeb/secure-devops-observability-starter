# Secure DevOps & DevSecOps Starter

A small portfolio project demonstrating a testable Flask service, Docker containerization, GitHub Actions CI, dependency auditing, container image scanning, and basic health/metrics endpoints.

> This repository is a starter/demo, not a production deployment template. Review dependency scan results and update pinned GitHub Actions before using it for real systems.

## Features

- Flask JSON API with `/`, `/health`, `/ready`, `/echo`, and `/metrics`
- Pytest automated tests
- Docker image runs as a non-root user
- Docker health check
- Compose example with read-only root filesystem, dropped Linux capabilities, and `no-new-privileges`
- GitHub Actions CI workflow that tests code and builds the image
- Separate security workflow using `pip-audit` and Trivy
- No cloud credentials required for CI

## Architecture

See [`docs/architecture.md`](docs/architecture.md).

## Run locally

Requirements: Python 3.12+, Docker, and Docker Compose plugin.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

Run with Docker:

```bash
docker build -t secure-devops-starter:local .
docker run --rm -p 8080:8080 secure-devops-starter:local
```

Or use Compose:

```bash
docker compose up --build
```

Try these endpoints:

```bash
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/ready
curl 'http://localhost:8080/echo?message=hello'
curl http://localhost:8080/metrics
```

Stop Compose with `docker compose down`.

## CI and security workflows

- `.github/workflows/ci.yml`: installs Python dependencies, runs tests, and builds a Docker image.
- `.github/workflows/security.yml`: runs `pip-audit` and Trivy scans on the image.

A security scan can fail because a dependency or base image has a known high/critical vulnerability. Read the report, update dependencies/base images intentionally, and rerun the workflow; do not simply disable the scan to make it green.

## Security notes

- Never commit `.env`, cloud keys, tokens, SSH private keys, or production data.
- Workflows use read-only repository permissions by default.
- The example workflows use GitHub-hosted runners. If you adapt this to a self-hosted runner, isolate it from untrusted pull requests and restrict repository/workflow access.
- Pin third-party actions to reviewed full commit SHAs for a higher-assurance production setup.
- Do not expose the Flask development server; the Docker image uses Gunicorn.
- `requirements.txt` includes pytest for CI; production image installs only `requirements-prod.txt`.
- `/metrics` exposes only demo metrics; it is not a complete Prometheus instrumentation implementation.
- Image scans may identify issues that require judgment. Review findings rather than claiming the app is vulnerability-free.

## Suggested next improvements

1. Add a deployment stage for a chosen target (for example, AWS EC2) with a documented authentication method.
2. Add integration tests and code coverage.
3. Add Terraform for reproducible infrastructure after learning state and IAM safety.
4. Add monitoring with Prometheus/Grafana or an AWS-native alternative.
5. Add a tested rollback strategy.
6. Consider SBOM generation and image signing.

## Portfolio evidence checklist

Before adding this project to your resume, personally run and verify:

- [ ] `pytest -q` passes
- [ ] `docker build -t secure-devops-starter:local .` succeeds
- [ ] `/health` returns HTTP 200 in the running container
- [ ] GitHub Actions CI workflow succeeds
- [ ] Dependency and image scan results are reviewed and documented
- [ ] README reflects what you actually tested

## Resume bullet (use only after verifying)

- Built a containerized Flask service with Docker and automated CI using GitHub Actions; added pytest checks, dependency auditing, Trivy image scanning, and health endpoints.

## License

Choose and add a license before accepting contributions or redistributing.
