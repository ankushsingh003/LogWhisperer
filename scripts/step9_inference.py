import torch
import json
import numpy as np
from step6_model import LogWhispererBrain
from step10_explainer import explain_prediction
from step11_remediation import suggest_remediation
from step12_notifier import send_alert

def run_inference(live_graph_data):
    """
    Simulates a real-time RCA inference run with Industrial Extensions.
    """
    print("--- LogWhisperer: Real-time RCA Run (Industrial) ---")
    
    # 1. Load the "Brain"
    FEATURE_DIM = 775
    model = LogWhispererBrain(in_channels=FEATURE_DIM, hidden_channels=16, out_channels=1)
    model.eval()

    # 2. Prepare Live Data
    nodes = live_graph_data['nodes']
    num_nodes = len(nodes)
    x = torch.tensor([n['feature_vector'] for n in nodes], dtype=torch.float)
    edge_index = torch.tensor([[i, (i+1)%num_nodes] for i in range(num_nodes)], dtype=torch.long).t()

    # 3. Predict Root Cause
    with torch.no_grad():
        logits = model(x, edge_index)
        probabilities = torch.sigmoid(logits).squeeze().numpy()

    # 4. Rank & Explain & Act
    rankings = []
    for i, prob in enumerate(probabilities):
        score = float(prob)
        service_id = nodes[i]['id']
        
        report = {
            "service": service_id,
            "score": score
        }
        
        if score > 0.8:
            # Step 10: Explain
            explanation = explain_prediction(service_id, x[i].numpy())
            report["explanation"] = explanation
            
            # Step 11: Remediation
            remediation = suggest_remediation(service_id, explanation)
            report["remediation"] = remediation
            
            # Step 12: Notification
            send_alert(report)
            
        rankings.append(report)

    # Sort by probability descending
    rankings = sorted(rankings, key=lambda x: x['score'], reverse=True)
    
    print("\n--- Final Rankings ---")
    for r in rankings:
        status = "🚨 ALERT" if r['score'] > 0.8 else "✅ OK"
        print(f"[{status}] {r['service']} (Score: {r['score']:.4f})")
    
    return rankings

if __name__ == "__main__":
    # Mock live data
    mock_live_data = {
        "nodes": [
            {"id": "auth-service", "feature_vector": np.random.randn(775).tolist()},
            {"id": "cart-service", "feature_vector": (np.random.randn(775) + 3.0).tolist()}, # FAILURE
            {"id": "payment-db", "feature_vector": np.random.randn(775).tolist()}
        ]
    }
    
    run_inference(mock_live_data)
