import requests
import json

# Test uploading a conversation
url = "http://127.0.0.1:8000/api/conversations/"
conversation_data = {
    "title": "Customer Support Chat",
    "messages": [
        {"sender": "user", "text": "Hi, I need help with my order."},
        {"sender": "ai", "text": "Sure, can you please share your order ID?"},
        {"sender": "user", "text": "It's 12345."},
        {"sender": "ai", "text": "Thanks! Your order has been shipped and will arrive tomorrow."}
    ]
}

try:
    response = requests.post(url, json=conversation_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

# Get all reports
print("\n--- Fetching Reports ---")
reports_url = "http://127.0.0.1:8000/api/reports/"
try:
    response = requests.get(reports_url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")