import numpy as np
import json

def encode_traces(traces):
    """
    Simulates encoding request paths (Traces) into fixed-length vectors.
    """
    print("Encoding traces...")
    
    # Map of operation names to integer IDs
    op_map = {"auth": 1, "cart": 2, "payment": 3, "db_query": 4, "retry": 5}
    
    encoded_features = []
    
    for trace in traces:
        path = trace['path']
        durations = trace['durations'] # ms per span
        
        # 1. Path Identity (Average ID) - simple representation
        path_ids = [op_map.get(op, 0) for op in path]
        path_score = np.mean(path_ids)
        
        # 2. Total Latency
        total_latency = np.sum(durations)
        
        # 3. Anomaly Heuristic: Retries detected?
        has_retry = 1.0 if "retry" in path else 0.0
        
        # Combined Trace Vector
        trace_vector = [path_score, total_latency, has_retry]
        encoded_features.append({
            "trace_id": trace["trace_id"],
            "vector": trace_vector
        })
        
    print("Success! Traces encoded.")
    return encoded_features

if __name__ == "__main__":
    # Mock Traces
    mock_traces = [
        {"trace_id": "T1", "path": ["auth", "cart", "payment"], "durations": [10, 20, 100]},
        {"trace_id": "T2", "path": ["auth", "cart", "payment", "retry", "payment"], "durations": [10, 20, 500, 100, 500]}, # ANOMALY
    ]
    
    results = encode_traces(mock_traces)
    
    for res in results:
        print(f"Trace {res['trace_id']} Vector: {res['vector']}")
        
    with open("trace_features.json", "w") as f:
        json.dump(results, f, indent=4)
