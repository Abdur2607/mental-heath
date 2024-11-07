from langchain_ollama import ChatOllama  # Updated import
from langchain_core.messages import HumanMessage, AIMessage

def chat_with_mistral():
    # Initialize the chat model with the latest package
    chat = ChatOllama(
        model="mistral",
        temperature=0.7
    )
    
    print("Starting chat with Mistral...")
    print("Type 'exit' to end the conversation")
    print("-" * 50)
    
    # Store conversation history
    history = []
    
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'exit':
            print("\nGoodbye!")
            break
            
        try:
            # Create message with history context
            messages = history + [HumanMessage(content=user_input)]
            
            # Get response
            response = chat.invoke(messages)
            
            # Print response
            print("\nMistral:", response.content)
            
            # Add to history
            history.append(HumanMessage(content=user_input))
            history.append(AIMessage(content=response.content))
            
            # Keep history to last 10 messages to avoid context length issues
            if len(history) > 10:
                history = history[-10:]
                
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Make sure Ollama is running and Mistral model is installed!")
            
if __name__ == "__main__":
    chat_with_mistral()