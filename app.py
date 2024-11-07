from flask import Flask, request, jsonify, make_response
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from flask_cors import CORS
import traceback

app = Flask(__name__)
# Enable CORS for all domains and methods
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

def create_system_message():
    """Create the initial system message for MotorMate"""
    return SystemMessage(content="""
    You are MotorMate, an expert automotive assistant with comprehensive knowledge about cars. Your capabilities include:

    1. Car Recommendations: You can suggest vehicles based on user preferences, budget, lifestyle, and needs.
    2. Car Comparisons: You can compare different car models across various parameters like performance, features, price, reliability, and value.
    3. Technical Knowledge: You can explain car specifications, features, and technical details in an easy-to-understand way.
    4. Market Insight: You have knowledge about current car market trends, pricing, and value propositions.
    5. Practical Advice: You can provide guidance on car maintenance, ownership costs, and practical considerations.
    6.Also keep your responses short , only givr big answers when the customer asks so 

    Guidelines for interaction:
    - Ask clarifying questions when needed to provide better recommendations
    - Provide balanced, objective comparisons
    - Include both pros and cons in your recommendations
    - Consider factors like budget, safety, reliability, and practical needs
    - Use your automotive expertise to explain technical concepts in simple terms
    - Keep responses concise but informative

    Remember: Your goal is to help users make informed decisions about their car choices while maintaining a helpful and professional demeanor.
    """)

def initialize_chat():
    """Initialize the chat model with appropriate parameters"""
    try:
        return ChatOllama(
            model="mistral",
            temperature=0.7,
            streaming=False
        )
    except Exception as e:
        print(f"Error initializing chat model: {str(e)}")
        raise

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST")
        return response

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Verify content type
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json',
                'success': False
            }), 415

        # Get data from request
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'error': 'No message provided',
                'success': False
            }), 400

        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify({
                'error': 'Empty message',
                'success': False
            }), 400

        # Initialize chat model
        chat_model = initialize_chat()

        # Create conversation history
        conversation = [create_system_message()]
        history = data.get('history', [])
        
        # Add previous messages if they exist
        for msg in history:
            if msg['type'] == 'human':
                conversation.append(HumanMessage(content=msg['content']))
            elif msg['type'] == 'ai':
                conversation.append(AIMessage(content=msg['content']))

        # Add new user message
        conversation.append(HumanMessage(content=user_message))

        try:
            # Get response from model
            response = chat_model.invoke(conversation)
            response_content = response.content

            # Format the conversation history
            current_history = [
                {'type': 'human', 'content': user_message},
                {'type': 'ai', 'content': response_content}
            ]

            return jsonify({
                'response': response_content,
                'history': history + current_history,
                'success': True
            })

        except Exception as chat_error:
            print(f"Error getting response from chat model: {str(chat_error)}")
            return jsonify({
                'error': 'Error generating response',
                'detail': str(chat_error),
                'success': False
            }), 500

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'error': 'An error occurred while processing your request. Please try again.',
            'detail': str(e),
            'success': False
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'success': False}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'success': False}), 500

if __name__ == '__main__':
    # Make sure Ollama is running before starting the server
    try:
        test_chat = initialize_chat()
        print("Successfully connected to Ollama")
        app.run(debug=True, host='127.0.0.1', port=5000)
    except Exception as e:
        print(f"Error: Could not initialize chat model. Make sure Ollama is running and the Mistral model is installed.")
        print(f"Error details: {str(e)}")