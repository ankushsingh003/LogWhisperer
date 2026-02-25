import torch
from step6_model import LogWhispererBrain
from step7_chaos_simulator import simulate_chaos

def train_brain():
    # 1. Hyperparameters
    FEATURE_DIM = 775
    HIDDEN_DIM = 16
    lr = 0.01
    epochs = 100
    
    # 2. Initialize Model & Optimizer
    model = LogWhispererBrain(in_channels=FEATURE_DIM, hidden_channels=HIDDEN_DIM, out_channels=1)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = torch.nn.BCEWithLogitsLoss()
    
    # 3. Training Loop
    model.train()
    print("Starting Training Loop...")
    
    mock_graph = {"nodes": [{"id": f"srv-{i}"} for i in range(10)], "edges": []}
    
    # Mock Edge Index (Fully connected for simplicity in mock)
    edge_index = torch.tensor([[0, 1], [1, 0]], dtype=torch.long) 
    
    for epoch in range(epochs):
        # Fresh Chaos injection per epoch
        x, y = simulate_chaos(mock_graph)
        y = y.view(-1, 1)
        
        optimizer.zero_grad()
        out = model(x, edge_index)
        loss = loss_fn(out, y)
        
        loss.backward()
        optimizer.step()
        
        if epoch % 10 == 0:
            print(f"Epoch {epoch} | Loss: {loss.item():.4f}")
            
    print("Training Complete. Model is now sensitive to system failures.")
    torch.save(model.state_dict(), "log_whisperer_v1.pth")

if __name__ == "__main__":
    train_brain()
