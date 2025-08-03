import os
from typing import Tuple

import joblib
import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split


EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "flight-model")
MODEL_NAME = os.getenv("MLFLOW_MODEL_NAME", "flight-model")
METRIC_THRESHOLD = float(os.getenv("MODEL_METRIC_THRESHOLD", "0.9"))


def load_data(path: str) -> Tuple[pd.DataFrame, pd.Series]:
    """Load dataset from a CSV file."""
    data = pd.read_csv(path)
    X = data.drop('target', axis=1)
    y = data['target']
    return X, y


def build_model() -> RandomForestClassifier:
    """Create the model instance using environment-provided hyperparameters."""
    return RandomForestClassifier(
        n_estimators=int(os.getenv("N_ESTIMATORS", "100")),
        max_depth=int(os.getenv("MAX_DEPTH", "5")),
        random_state=42,
    )


def train_model(model: RandomForestClassifier, X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
    """Train the model."""
    model.fit(X_train, y_train)
    return model


def evaluate_model(
    model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series
) -> Tuple[float, float]:
    """Evaluate the model and return accuracy and F1 score."""
    predictions = model.predict(X_test)
    return accuracy_score(y_test, predictions), f1_score(y_test, predictions, average="macro")


def save_model(model: RandomForestClassifier, output_path: str) -> None:
    """Persist the trained model to disk."""
    joblib.dump(model, output_path)


def main() -> None:
    data_path = os.getenv("TRAINING_DATA", "data.csv")
    model_output = os.getenv("MODEL_OUTPUT", "model.joblib")

    X, y = load_data(data_path)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
    mlflow.set_experiment(EXPERIMENT_NAME)

    with mlflow.start_run() as run:
        model = build_model()
        model = train_model(model, X_train, y_train)

        accuracy, f1 = evaluate_model(model, X_test, y_test)
        print(f"accuracy={accuracy}")

        mlflow.log_params({"n_estimators": model.n_estimators, "max_depth": model.max_depth})
        mlflow.log_metrics({"accuracy": accuracy, "f1": f1})
        mlflow.sklearn.log_model(model, "model")
        if accuracy >= METRIC_THRESHOLD or f1 >= METRIC_THRESHOLD:
            mlflow.register_model(f"runs:/{run.info.run_id}/model", MODEL_NAME)

    save_model(model, model_output)


if __name__ == "__main__":
    main()
