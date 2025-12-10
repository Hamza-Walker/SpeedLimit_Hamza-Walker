
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import joblib
import os

def train_nn_model():
    """
    Loads processed data, trains a neural network to predict near-accidents,
    and saves the trained model.
    """
    # Load processed data
    try:
        data = pd.read_csv('data/processed/processed_data.csv', index_col='datetime', parse_dates=True)
    except FileNotFoundError:
        print("Error: Processed data not found. Please run data_preprocessing.py first.")
        return

    # Prepare features (X) and target (y)
    # Features: humidity, light, noise, temperature, traffic, wind direction, wind strength, water
    # Target: near_accidents
    features = ['humidity', 'light', 'noise', 'temperature', 'traffic', 'wind direction', 'wind strength', 'water']
    X = data[features].values
    y = data['near_accidents'].values

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("Data prepared and scaled.")
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)

    # Save the scaler
    scaler_path = 'models/scaler.pkl'
    joblib.dump(scaler, scaler_path)
    print(f"Scaler saved to {scaler_path}")

    # --- Neural Network Model Definition and Training ---
    model = Sequential([
        Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)),
        Dense(32, activation='relu'),
        Dense(1, activation='relu') # Output layer for near_accidents count (non-negative)
    ])

    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    print("Neural Network model compiled.")

    # Train the model
    history = model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, validation_split=0.1, verbose=2)
    print("Neural Network model trained.")

    # Evaluate the model
    loss, mae = model.evaluate(X_test_scaled, y_test, verbose=0)
    print(f"Model Evaluation: MAE = {mae:.4f}")

    # Save the trained model
    model_path = 'models/nn_model.keras'
    model.save(model_path)
    print(f"Trained Neural Network model saved to {model_path}")


if __name__ == '__main__':
    train_nn_model()
