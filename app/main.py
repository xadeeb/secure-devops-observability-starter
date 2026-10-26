"""Small demo service for the Secure DevOps Starter project."""
import os
import time
import logging
from flask import Flask, jsonify, request

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(message)s",
)
app = Flask(__name__)
START_TIME = time.time()
VERSION = os.getenv("APP_VERSION", "dev")


@app.get("/")
def home():
    return jsonify({
        "service": "secure-devops-starter",
        "status": "ok",
        "version": VERSION,
        "message": "Deployment and observability demo service",
    })


@app.get("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.get("/ready")
def ready():
    return jsonify({"status": "ready", "uptime_seconds": int(time.time() - START_TIME)}), 200


@app.get("/echo")
def echo():
    # Intentionally accepts only a small, safe set of query parameters.
    message = request.args.get("message", "")
    if len(message) > 200:
        return jsonify({"error": "message must be 200 characters or fewer"}), 400
    app.logger.info("echo endpoint called; message_length=%d", len(message))
    return jsonify({"message": message})


@app.get("/metrics")
def metrics():
    # Minimal demo metrics in Prometheus text exposition format.
    uptime = int(time.time() - START_TIME)
    body = (
        "# HELP demo_service_up Whether the demo service is responding.\n"
        "# TYPE demo_service_up gauge\n"
        "demo_service_up 1\n"
        "# HELP demo_service_uptime_seconds Service uptime in seconds.\n"
        "# TYPE demo_service_uptime_seconds counter\n"
        f"demo_service_uptime_seconds {uptime}\n"
    )
    return body, 200, {"Content-Type": "text/plain; version=0.0.4; charset=utf-8"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
