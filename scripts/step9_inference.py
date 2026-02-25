import torch
import json
import numpy as np
from step6_model import LogWhispererBrain

def run_inference(live_graph_data):
    """
    Simulates a real-time RCA inference run.
    """
    print("--- LogWhisperer: Real-time RCA Run ---")
    
    # 1. Load the "Brain"
    FEATURE_DIM = 775
    model = LogWhispererBrain(in_channels=FEATURE_DIM, hidden_channels=16, out_channels=1)
    
    # Load trained weights (using mock for demonstration)
    # model.load_state_dict(torch.load("log_whisperer_v1.pth"))
    model.eval()

    # 2. Prepare Live Data
    nodes = live_graph_data['nodes']
    num_nodes = len(nodes)
    
    # Convert feature vectors to tensor
    x = torch.tensor([n['feature_vector'] for n in nodes], dtype=torch.float)
    
    # Mock Edge Index (assuming linear connectivity for mock)
    edge_index = torch.tensor([[i, (i+1)%num_nodes] for i in range(num_nodes)], dtype=torch.long).t()

    # 3. Predict Root Cause
    with torch.no_grad():
        logits = model(x, edge_index)
        probabilities = torch.sigmoid(logits).squeeze().numpy()

    # 4. Rank & Report
    rankings = []
    for i, prob in enumerate(probabilities):
        rankings.append({
            "service": nodes[i]['id'],
            "score": float(prob)
        })

    # Sort by probability descending
    rankings = sorted(rankings, key=lambda x: x['score'], reverse=True)
    
    print("\nRoot Cause Investigation Results:")
    for rank in rankings:
        status = "🚨 ROOT CAUSE SUSPECT" if rank['score'] > 0.8 else "✅ Healthy"
        print(f"[{status}] Service: {rank['service']} | Score: {rank['score']:.4f}")
    
    return rankings

if __name__ == "__main__":
    # Mock live data coming from graph_builder.py
    mock_live_data = {
        "nodes": [
            {"id": "auth-service", "feature_vector": np.random.randn(775).tolist()},
            {"id": "cart-service", "feature_vector": (np.random.randn(775) + 3.0).tolist()}, # SIMULATED FAILURE
            {"id": "payment-db", "feature_vector": np.random.randn(775).tolist()}
        ]
    }
    
    run_inference(mock_live_data)
