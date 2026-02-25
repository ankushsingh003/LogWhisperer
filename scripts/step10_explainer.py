import torch
import numpy as np

def explain_prediction(node_index, feature_vector):
    """
    Simulates finding 'Feature Importance' using gradients or simple saliency.
    """
    print(f"Generating Explanation for Node {node_index}...")
    
    # Feature map for human-readable output
    # Index 0-767: Log BERT, 768-771: Metrics, 772-774: Traces
    
    # In a real model, we would use torch.autograd to find which feature 
    # has the highest gradient. Here we mock it by finding the highest value.
    top_feature_index = np.argmax(np.abs(feature_vector))
    
    explanation = ""
    if top_feature_index < 768:
        explanation = "High Semantic Match: Detected anomalous Log Patterns (Logs)."
    elif 768 <= top_feature_index < 772:
        explanation = "Numerical Anomaly: Significant spike in Service Metrics (CPU/Latency)."
    else:
        explanation = "Path Anomaly: Unusual Request Trace sequence detected."
        
    return explanation

if __name__ == "__main__":
    # Mock feature vector with a spike in the Metric region (Index 769)
    mock_vector = np.zeros(775)
    mock_vector[769] = 10.0 # Huge spike in CPU
    
    reason = explain_prediction("payment-service", mock_vector)
    print(f"AI Decision: {reason}")
