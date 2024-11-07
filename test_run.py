import requests
import json
import sys

def chat_with_local_mistral():
    """
    Chat with locally downloaded Mistral model through Ollama with real-time streaming
    """
    print("Starting chat with local Mistral model...")
    print("Type 'exit' to end the conversation")
    print("-" * 50)

    # Ollama runs locally on port 11434 by default
    url = "http://localhost:11434/api/generate"

    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        try:
            # Send request to local Ollama instance
            response = requests.post(url, 
                json={
                    "model": "mistral",
                    "prompt": user_input,
                    "stream": True
                },
                stream=True
            )
            
            if response.status_code == 200:
                print("\nMistral:", end=" ", flush=True)
                # Process the streaming response
                for line in response.iter_lines():
                    if line:
                        json_response = json.loads(line)
                        if 'response' in json_response:
                            print(json_response['response'], end="", flush=True)
                print()  # New line after response is complete
            else:
                print(f"Error: Received status code {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("\nError: Cannot connect to Ollama. Make sure Ollama is running!")
            print("You can start it by opening a terminal and typing: 'ollama serve'")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    chat_with_local_mistral()