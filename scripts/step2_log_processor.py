import torch
from transformers import AutoTokenizer, AutoModel
import re
import json

# Configuration
MODEL_NAME = "distilbert-base-uncased" # Using DistilBERT as a representative base for LogBERT
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

def extract_template(log_message):
    """
    Mock template extractor. 
    In industry, tools like Drain or MoLFI are used.
    """
    # Replace common variable patterns with placeholders
    log_message = re.sub(r'\d+', '<ID>', log_message)
    log_message = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '<IP>', log_message)
    return log_message

def get_log_embedding(template):
    """
    Converts a log template into a 768-dimensional vector.
    """
    inputs = tokenizer(template, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Use Mean Pooling to get a single vector for the sentence
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.squeeze().numpy()

def process_logs(sample_logs):
    print(f"Processing {len(sample_logs)} logs...")
    features = {}
    
    for log in sample_logs:
        template = extract_template(log)
        embedding = get_log_embedding(template)
        
        # In a real system, we aggregate these per service_name
        features[log] = embedding.tolist()
        
    print("Success! Logs embedded into vectors.")
    return features

if __name__ == "__main__":
    test_logs = [
        "Connection refused to 192.168.1.10",
        "NullPointerException at com.app.Service.execute",
        "User 501 logged in successfully",
        "Read timed out from database cluster"
    ]
    
    results = process_logs(test_logs)
    
    # Show first few dims of first log
    first_log = test_logs[0]
    print(f"\nExample Log: {first_log}")
    print(f"Embedding (first 5 dims): {results[first_log][:5]}...")
    
    # Save to file
    with open("log_features.json", "w") as f:
        json.dump(results, f)
