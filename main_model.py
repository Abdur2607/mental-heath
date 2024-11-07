from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

def create_motormate():
    # System message defining MotorMate's role and capabilities
    system_message = SystemMessage(content="""
You are MotorMate, an expert automotive assistant with comprehensive knowledge about cars. Your capabilities include:

1. Car Recommendations: You can suggest vehicles based on user preferences, budget, lifestyle, and needs.
2. Car Comparisons: You can compare different car models across various parameters like performance, features, price, reliability, and value.
3. Technical Knowledge: You can explain car specifications, features, and technical details in an easy-to-understand way.
4. Market Insight: You have knowledge about current car market trends, pricing, and value propositions.
5. Practical Advice: You can provide guidance on car maintenance, ownership costs, and practical considerations.

Guidelines for interaction:
- Always introduce yourself as MotorMate when meeting a new user
- Ask clarifying questions when needed to provide better recommendations
- Provide balanced, objective comparisons
- Include both pros and cons in your recommendations
- Consider factors like budget, safety, reliability, and practical needs
- Use your automotive expertise to explain technical concepts in simple terms

Remember: Your goal is to help users make informed decisions about their car choices while maintaining a helpful and professional demeanor.
""")
    
    return system_message

def chat_with_motormate():
    # Initialize the chat model
    chat = ChatOllama(
        model="mistral",
        temperature=0.7
    )
    
    print("Welcome to MotorMate - Your Automotive Assistant!")
    print("Ask me anything about cars, recommendations, or comparisons.")
    print("Type 'exit' to end the conversation")
    print("-" * 50)
    
    # Initialize history with system message
    system_message = create_motormate()
    history = [system_message]
    
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'exit':
            print("\nThank you for using MotorMate! Have a great day!")
            break
            
        try:
            # Create message with history context
            messages = history + [HumanMessage(content=user_input)]
            
            # Get response
            response = chat.invoke(messages)
            
            # Print response
            print("\nMotorMate:", response.content)
            
            # Add to history
            history.append(HumanMessage(content=user_input))
            history.append(AIMessage(content=response.content))
            
            # Keep history to last 10 messages (plus system message)
            if len(history) > 11:  # 1 system message + 10 conversation messages
                history = [system_message] + history[-10:]
                
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Make sure Ollama is running and Mistral model is installed!")
            
if __name__ == "__main__":
    chat_with_motormate()