import json
import numpy as np

def build_rca_graph():
    """
    Integrates topology, logs, metrics, and traces into a single graph.
    """
    print("Building RCA Graph...")
    
    # 1. Load Topology (Phase 1)
    try:
        with open("topology_graph.json", "r") as f:
            topology = json.load(f)
    except FileNotFoundError:
        print("Topology data not found. Using mock nodes.")
        topology = {"nodes": ["auth", "cart", "payment"], "edges": [{"source": "auth", "target": "cart"}]}

    # 2. Load Features (Phase 2)
    # Mocking data that would be produced by log_processor.py, metric_analyzer.py, etc.
    # In a real system, these would be loaded from .json files generated in Phase 2
    
    # Mock Log Vectors (768 dims, simplified here)
    log_features = {node: np.random.randn(8).tolist() for node in topology["nodes"]}
    
    # Mock Metric Vectors (Normalized)
    metric_features = {node: [np.random.normal(), np.random.normal()] for node in topology["nodes"]}
    
    # 3. Graph Assembly
    rca_graph = {
        "nodes": [],
        "edges": topology["edges"]
    }
    
    for node_name in topology["nodes"]:
        # NODE ATTRIBUTE FUSION (Phase 3.2 conceptually)
        # Concatenate Log + Metric features
        combined_vector = log_features[node_name] + metric_features[node_name]
        
        rca_graph["nodes"].append({
            "id": node_name,
            "feature_vector": combined_vector
        })
    
    # Save the final GNN input
    with open("gnn_input_graph.json", "w") as f:
        json.dump(rca_graph, f, indent=4)
        
    print(f"Success! RCA Graph built with {len(rca_graph['nodes'])} nodes.")
    print(f"Node Vector Dimension: {len(rca_graph['nodes'][0]['feature_vector'])}")
    return rca_graph

if __name__ == "__main__":
    build_rca_graph()
