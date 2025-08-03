import os
from typing import Tuple

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


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


def evaluate_model(model: RandomForestClassifier, X_test: pd.DataFrame, y_test: pd.Series) -> float:
    """Evaluate the model and return the accuracy."""
    predictions = model.predict(X_test)
    return accuracy_score(y_test, predictions)


def save_model(model: RandomForestClassifier, output_path: str) -> None:
    """Persist the trained model to disk."""
    joblib.dump(model, output_path)


def main() -> None:
    data_path = os.getenv("TRAINING_DATA", "data.csv")
    model_output = os.getenv("MODEL_OUTPUT", "model.joblib")

    X, y = load_data(data_path)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = build_model()
    model = train_model(model, X_train, y_train)

    accuracy = evaluate_model(model, X_test, y_test)
    print(f"accuracy={accuracy}")

    save_model(model, model_output)


if __name__ == "__main__":
    main()
