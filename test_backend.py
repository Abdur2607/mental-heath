import requests
import json
import time

def test_chat():
    url = "http://127.0.0.1:5000/chat"
    headers = {
        "Content-Type": "application/json"
    }
    test_message = "Hi, can you help me find a good family car?"
    
    data = {
        "message": test_message,
        "history": []
    }

    print("\nTesting MotorMate Backend...")
    print(f"\nSending test message: '{test_message}'")
    
    try:
        # Add a small delay to ensure server is ready
        time.sleep(1)
        
        # Send the request
        response = requests.post(url, headers=headers, json=data)
        
        print("\nResponse Status Code:", response.status_code)
        print("\nResponse Headers:")
        print(json.dumps(dict(response.headers), indent=2))
        
        if response.status_code == 200:
            response_data = response.json()
            print("\nResponse Content:")
            print(json.dumps(response_data, indent=2))
            print("\n✅ Test successful! Backend is working correctly.")
            return True
        else:
            print("\nResponse Error:")
            print(json.dumps(response.json(), indent=2))
            print("\n❌ Test failed! Backend returned an error.")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the server. Make sure the Flask server is running on port 5000.")
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_chat()