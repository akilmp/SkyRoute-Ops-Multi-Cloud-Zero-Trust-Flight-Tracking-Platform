"""Simple training pipeline for demonstration."""
import os

import mlflow
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

EXPERIMENT_NAME = "flight-model"
MODEL_NAME = "flight-model"


def main() -> None:
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
    mlflow.set_experiment(EXPERIMENT_NAME)
    with mlflow.start_run() as run:
        data = load_iris(as_frame=True)
        X_train, X_test, y_train, y_test = train_test_split(
            data.data, data.target, test_size=0.2, random_state=42
        )
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        f1 = f1_score(y_test, preds, average="macro")
        mlflow.log_metric("f1", f1)
        mlflow.sklearn.log_model(model, "model")
        if f1 >= 0.85:
            mlflow.register_model(
                f"runs:/{run.info.run_id}/model", MODEL_NAME
            )
        print(f"F1 score: {f1:.4f}")


if __name__ == "__main__":
    main()
