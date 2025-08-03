import os
import sys

import mlflow


def main() -> None:
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    model_name = os.getenv("MLFLOW_MODEL_NAME", "flight-model")
    client = mlflow.MlflowClient(tracking_uri)
    try:
        client.get_registered_model(model_name)
    except Exception as exc:
        print(f"Model '{model_name}' not registered: {exc}", file=sys.stderr)
        sys.exit(1)
    print(f"Model '{model_name}' is registered")


if __name__ == "__main__":
    main()
