# LogWhisperer: Automated RCA System

This project implements an Automated Root Cause Analysis (RCA) system using Deep Learning (GNNs).

## Phase 1: Service Mesh & Topology
This phase sets up the data foundation by integrating a service mesh to capture live microservice traffic.

### Components
- `infra/istio-config.yaml`: Configuration for Istio sidecar injection and telemetry.
- `infra/fluent-bit-config.yaml`: Configuration for log collection & label tagging (Loki).
- `infra/prometheus-rules.yaml`: Pre-calculated RCA features (Error rates, P99 latency).
- `scripts/extract_topology.py`: Query Prometheus for the Service Graph.
- `scripts/log_processor.py`: Convert raw logs into semantic vectors using LogBERT.
- `scripts/metric_analyzer.py`: Normalize & scale Prometheus metrics (Z-score).
- `scripts/trace_encoder.py`: Encode request paths into trace vectors.
- `scripts/graph_builder.py`: Fuses topology and multi-modal features into a GNN-ready graph.
- `scripts/model.py`: The GAT (Graph Attention Network) brain of LogWhisperer (Phase 4).
- `scripts/chaos_simulator.py`: Injects "Chaos" events to generate training labels.
- `scripts/train.py`: The training loop that teaches the model to identify root causes.
- `requirements.txt`: Python dependencies.

### Getting Started
1. Install Istio on your Kubernetes cluster.
2. Apply the labels to your namespace: `kubectl label namespace <ns> istio-injection=enabled`.
3. Run the topology extractor to see your live service graph.
