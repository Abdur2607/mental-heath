const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('search-button');

// Initialize conversation history
let history = [];

// Add loading indicator function
function showLoadingIndicator() {
    const loadingDiv = document.createElement('div');
    loadingDiv.classList.add('bot-message', 'loading');
    loadingDiv.textContent = 'Bot: Thinking...';
    loadingDiv.id = 'loading-indicator';
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Remove loading indicator function
function removeLoadingIndicator() {
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.remove();
    }
}

// Function to enable/disable input during processing
function setInputState(disabled) {
    userInput.disabled = disabled;
    sendButton.disabled = disabled;
}

// Enhanced send response function
async function sendResponse() {
    const userMessage = userInput.value.trim();

    if (userMessage) {
        try {
            // Disable input while processing
            setInputState(true);
            
            // Add user message to chat
            const userMessageDiv = document.createElement('div');
            userMessageDiv.classList.add('user-message');
            userMessageDiv.textContent = `You: ${userMessage}`;
            chatMessages.appendChild(userMessageDiv);

            // Clear input and show loading
            userInput.value = '';
            showLoadingIndicator();

            // Send request to backend
            const response = await fetch('http://127.0.0.1:5000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    message: userMessage, 
                    history: history 
                }),
            });

            // Remove loading indicator
            removeLoadingIndicator();

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Update history
            history = data.history;

            // Add bot response
            const botMessage = document.createElement('div');
            botMessage.classList.add('bot-message');
            botMessage.textContent = `Bot: ${data.response}`;
            chatMessages.appendChild(botMessage);

        } catch (error) {
            console.error('Error:', error);
            const errorMessageDiv = document.createElement('div');
            errorMessageDiv.classList.add('error-message');
            errorMessageDiv.textContent = 'Sorry, something went wrong. Please try again later.';
            chatMessages.appendChild(errorMessageDiv);
        } finally {
            // Re-enable input
            setInputState(false);
            // Scroll to bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
}

// Add event listeners
sendButton.addEventListener('click', sendResponse);

userInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendResponse();
    }
});

// Add initial greeting when page loads
window.addEventListener('load', () => {
    const welcomeMessage = document.createElement('div');
    welcomeMessage.classList.add('bot-message');
    welcomeMessage.textContent = 'Bot: Hello! I\'m MotorMate, your automotive expert. How can I help you find your perfect car today?';
    chatMessages.appendChild(welcomeMessage);
});