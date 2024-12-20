import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.impute import SimpleImputer
import joblib
import os


# Function to load preprocessed data from multiple files
def load_data(file_paths):
    dataframes = [pd.read_csv(file) for file in file_paths]
    combined_df = pd.concat(dataframes, axis=0, ignore_index=True)
    X = combined_df.iloc[:, :-1].values
    y = combined_df.iloc[:, -1].values
    return X, y


# Function to handle missing values using SimpleImputer
def handle_missing_values(X):
    imputer = SimpleImputer(strategy="mean")
    X_imputed = imputer.fit_transform(X)
    return X_imputed


# Function to train Voting Classifier with multiple base estimators
def train_voting_classifier(X_train, y_train):

    # Define base estimators
    estimator1 = DecisionTreeClassifier(max_depth=2)
    estimator2 = RandomForestClassifier(n_estimators=70)
    estimator3 = LogisticRegression(max_iter=100)

    # Create the Voting Classifier
    voting_model = VotingClassifier(
        estimators=[("dt", estimator1), ("rf", estimator2), ("lr", estimator3)],
        voting="soft",  # We use soft voting for probability-based combination
    )

    # Train the model
    voting_model.fit(X_train, y_train)
    return voting_model


# Evaluate the model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))


# Main function
def main():
    # Paths to your preprocessed CSV files
    file_paths = [
        "data/AppGallery_preprocessed.csv",
        "data/Purchasing_preprocessed.csv",
    ]

    # Load the data
    print("Loading data from files...")
    X, y = load_data(file_paths)

    # Handle missing values in the data
    print("Handling missing values...")
    X = handle_missing_values(X)

    # Split the data into training and testing sets
    print("Splitting data into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y
    )

    # Train the Voting Classifier
    print("Training Voting classifier...")
    model = train_voting_classifier(X_train, y_train)

    # Evaluate the model
    print("Evaluating the model...")
    evaluate_model(model, X_test, y_test)

    # Save the model
    model_path = os.path.join("src", "models", "voting", "voting_model.pkl")
    print(f"Saving the model to {model_path}...")
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")


# Run the script
if __name__ == "__main__":
    main()
