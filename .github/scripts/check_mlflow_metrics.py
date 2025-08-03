import os
import sys

import mlflow


def main() -> None:
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    client = mlflow.MlflowClient(tracking_uri)
    experiment = client.get_experiment_by_name("flight-model")
    if experiment is None:
        print("Experiment 'flight-model' not found", file=sys.stderr)
        sys.exit(1)
    runs = client.search_runs(
        [experiment.experiment_id],
        order_by=["attributes.start_time DESC"],
        max_results=1,
    )
    if not runs:
        print("No runs found", file=sys.stderr)
        sys.exit(1)
    run = runs[0]
    f1 = run.data.metrics.get("f1")
    if f1 is None:
        print("F1 metric not logged", file=sys.stderr)
        sys.exit(1)
    threshold = float(os.getenv("F1_THRESHOLD", "0.85"))
    if f1 < threshold:
        print(f"Latest model F1 {f1:.4f} below threshold {threshold}", file=sys.stderr)
        sys.exit(1)
    print(f"Latest model F1 {f1:.4f} meets threshold {threshold}")


if __name__ == "__main__":
    main()
