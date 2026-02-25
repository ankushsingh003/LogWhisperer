import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import json

def normalize_metrics(raw_data):
    """
    Transforms raw Prometheus metrics into normalized feature vectors.
    """
    print("Normalizing metrics...")
    
    # Convert to DataFrame
    df = pd.DataFrame(raw_data)
    
    # 1. Handling Missing Values (Imputation)
    # If a service stops reporting, we forward-fill the last known state
    df = df.fillna(method='ffill').fillna(0)
    
    # 2. Extract numeric columns for scaling
    numeric_cols = ['cpu_usage', 'memory_usage', 'latency_ms', 'error_rate']
    
    # 3. Z-Score Scaling
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    
    print("Success! Metrics scaled to Mean=0, StdDev=1.")
    return df

if __name__ == "__main__":
    # Mock data representing metrics for 3 services over 5 time steps
    mock_metrics = [
        {"timestamp": 1, "service": "auth", "cpu_usage": 10, "memory_usage": 200, "latency_ms": 50, "error_rate": 0.01},
        {"timestamp": 1, "service": "cart", "cpu_usage": 15, "memory_usage": 300, "latency_ms": 60, "error_rate": 0.02},
        {"timestamp": 2, "service": "auth", "cpu_usage": 80, "memory_usage": 210, "latency_ms": 500, "error_rate": 0.05}, # SPIKE
        {"timestamp": 2, "service": "cart", "cpu_usage": 18, "memory_usage": 310, "latency_ms": 70, "error_rate": 0.02},
        {"timestamp": 3, "service": "auth", "cpu_usage": 95, "memory_usage": 220, "latency_ms": 1200, "error_rate": 0.10}, # FAILURE
    ]
    
    normalized_df = normalize_metrics(mock_metrics)
    
    print("\n--- Normalized Data Preview ---")
    print(normalized_df.head())
    
    # Convert to JSON features for the GNN
    features = normalized_df.to_dict(orient='records')
    with open("metric_features.json", "w") as f:
        json.dump(features, f, indent=4)
