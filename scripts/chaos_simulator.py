import numpy as np
import torch

def simulate_chaos(graph):
    """
    Simulates a 'Fault Injection' (Chaos Engineering) session.
    It picks a service as the root cause, injects jitter into its features,
    and returns the labels for training.
    """
    print("Simulating Chaos...")
    
    num_nodes = len(graph['nodes'])
    root_cause_index = np.random.randint(0, num_nodes)
    target_service = graph['nodes'][root_cause_index]['id']
    
    print(f"Injecting failure into: {target_service}")
    
    # 1. Generate Labels (y)
    # 1 for Root Cause, 0 for healthy or cascading failure
    labels = torch.zeros(num_nodes, dtype=torch.float)
    labels[root_cause_index] = 1.0
    
    # 2. Inject Semantic Jitter into Feature Matrix (X)
    # We simulate a failure by spiking the latent features of the target node
    x = torch.randn(num_nodes, 775)
    x[root_cause_index] += 5.0 # Distinctive spike for root cause
    
    # Simulate propagation (neighbors also get slightly "sick")
    for edge in graph['edges']:
        if edge['source'] == target_service:
            # Find the index of target service workload
            # For simplicity in this mock, we skip complex matching
            pass

    print("Chaos data generated.")
    return x, labels

if __name__ == "__main__":
    mock_graph = {"nodes": [{"id": "auth"}, {"id": "cart"}, {"id": "db"}], "edges": []}
    x, y = simulate_chaos(mock_graph)
    print(f"Labels: {y}")
