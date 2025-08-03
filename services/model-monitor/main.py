import os
import signal
import time
import threading
import pandas as pd
from prometheus_client import Gauge, start_http_server
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

METRICS_PORT = int(os.getenv("METRICS_PORT", "8000"))
BASELINE_PATH = os.getenv("BASELINE_PATH", "/data/baseline.csv")
RECENT_PATH = os.getenv("RECENT_PATH", "/data/recent.csv")
SLEEP_SECONDS = int(os.getenv("SLEEP_SECONDS", "30"))

# Prometheus metrics
DRIFT_SHARE = Gauge("model_drift_share", "Share of features with detected drift")
DRIFT_DETECTED = Gauge("model_drift_detected", "Whether dataset drift was detected (1=yes)")


stop_event = threading.Event()


def _handle_sigterm(signum, frame):
    """Signal handler to initiate graceful shutdown."""
    stop_event.set()


signal.signal(signal.SIGTERM, _handle_sigterm)


def compute_drift():
    """Run Evidently data drift report and update Prometheus metrics."""
    baseline = pd.read_csv(BASELINE_PATH)
    recent = pd.read_csv(RECENT_PATH)

    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=baseline, current_data=recent)
    summary = report.as_dict()["metrics"][0]["result"]["dataset_drift"]

    DRIFT_SHARE.set(summary["share_drifted_columns"])
    DRIFT_DETECTED.set(1 if summary["dataset_drift"] else 0)


def main() -> None:
    start_http_server(METRICS_PORT)
    while not stop_event.is_set():
        compute_drift()
        stop_event.wait(SLEEP_SECONDS)


if __name__ == "__main__":
    main()
