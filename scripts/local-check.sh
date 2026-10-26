#!/usr/bin/env bash
set -euo pipefail

python -m pip install -r requirements.txt
pytest -q
docker build -t secure-devops-starter:local .
docker run --rm -d --name secure-devops-starter-check -p 8080:8080 secure-devops-starter:local
cleanup() {
  docker rm -f secure-devops-starter-check >/dev/null 2>&1 || true
}
trap cleanup EXIT

for attempt in $(seq 1 20); do
  if curl --fail --silent http://127.0.0.1:8080/health >/dev/null; then
    echo "Health check passed."
    exit 0
  fi
  sleep 2
done

echo "Health check failed."
docker logs secure-devops-starter-check
exit 1
