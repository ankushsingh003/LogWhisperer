import torch
import torch.nn.functional as F
from torch_geometric.nn import GATConv

class LogWhispererBrain(torch.nn.Module):
    """
    LogWhisperer GNN Brain: A Graph Attention Network (GAT)
    that identifies root causes by attending to anomalous neighborhood features.
    """
    def __init__(self, in_channels, hidden_channels, out_channels, heads=4):
        super(LogWhispererBrain, self).__init__()
        
        # Layer 1: Graph Attention Convolution (with Multi-head attention)
        # in_channels = size of Log + Metric + Trace vector
        self.conv1 = GATConv(in_channels, hidden_channels, heads=heads, dropout=0.6)
        
        # Layer 2: Aggregated GAT layer
        # Concatenates output from heads of layer 1
        self.conv2 = GATConv(hidden_channels * heads, out_channels, heads=1, concat=False, dropout=0.6)

    def forward(self, x, edge_index):
        # x: Node Feature Matrix [N, D]
        # edge_index: Graph Connectivity Matrix [2, E]
        
        # 1. Apply first GAT layer with ELU activation
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv1(x, edge_index)
        x = F.elu(x)
        
        # 2. Apply final GAT layer (output is the logit for each service)
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv2(x, edge_index)
        
        # Output is a score for each node [N, out_channels]
        # We use out_channels = 1 for binary anomaly detection per node
        return x

if __name__ == "__main__":
    # Mock parameters
    FEATURE_DIM = 775 # Log(768) + Metrics(4) + Trace(3)
    
    model = LogWhispererBrain(in_channels=FEATURE_DIM, hidden_channels=16, out_channels=1)
    print("LogWhisperer Brain Initialized.")
    print(model)
