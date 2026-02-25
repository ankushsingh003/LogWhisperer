import requests
import json
import pandas as pd

# Configuration
PROMETHEUS_URL = "http://localhost:9090"  # Update to your Prometheus service URL
QUERY = 'istio_requests_total{reporter="destination"}'

def fetch_topology():
    print(f"Fetching topology from {PROMETHEUS_URL}...")
    try:
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={'query': QUERY})
        results = response.json()['data']['result']
        
        edges = []
        nodes = set()
        
        for result in results:
            metric = result['metric']
            source = metric.get('source_workload', 'unknown')
            dest = metric.get('destination_workload', 'unknown')
            rps = result['value'][1]
            
            nodes.add(source)
            nodes.add(dest)
            edges.append({
                "source": source,
                "target": dest,
                "requests_per_second": rps
            })
            
        topology = {
            "nodes": list(nodes),
            "edges": edges
        }
        
        with open("topology_graph.json", "w") as f:
            json.dump(topology, f, indent=4)
            
        print("Success! Topology saved to topology_graph.json")
        print(f"Discovered {len(nodes)} nodes and {len(edges)} edges.")
        
    except Exception as e:
        print(f"Error connecting to Prometheus: {e}")

if __name__ == "__main__":
    fetch_topology()
