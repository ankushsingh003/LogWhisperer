import json
import requests

def send_alert(rca_report, webhook_url=None):
    """
    Industrial Notification Hub:
    Sends structured RCA reports to Slack, Microsoft Teams, or custom webhooks.
    """
    print("--- Notification Hub: Dispatching Alerts ---")
    
    # Format the payload for Slack/JSON webhook
    payload = {
        "text": "🚨 *LogWhisperer Incident Report*",
        "attachments": [
            {
                "color": "#ff0000",
                "fields": [
                    {"title": "Root Cause", "value": rca_report['service'], "short": True},
                    {"title": "Confidence", "value": f"{rca_report['score']:.2%}", "short": True},
                    {"title": "Explanation", "value": rca_report['explanation'], "short": False},
                    {"title": "Remediation", "value": f"`{rca_report['remediation']['suggested_command']}`", "short": False}
                ],
                "footer": "LogWhisperer RCA Bot",
                "ts": 1625000000
            }
        ]
    }

    if webhook_url:
        print(f"Post data to: {webhook_url}")
        # In a real scenario: requests.post(webhook_url, json=payload)
    else:
        print("MOCK ALERT: (Specify SLACK_WEBHOOK to enable live alerts)")
        print(json.dumps(payload, indent=2))
        
    return payload

if __name__ == "__main__":
    mock_report = {
        "service": "cart-service",
        "score": 0.985,
        "explanation": "Numerical Anomaly: Significant spike in Service Metrics.",
        "remediation": {"suggested_command": "kubectl scale deployment/cart-service --replicas=5"}
    }
    send_alert(mock_report)
