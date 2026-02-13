const chatBox = document.getElementById('chat-box');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');

// Scroll to bottom functionality
function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Add message to chat UI
function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'avatar';
    avatarDiv.textContent = isUser ? 'You' : 'IA';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    // Simple text handling; could be expanded to support HTML/Markdown
    const p = document.createElement('p');
    p.textContent = content;
    contentDiv.appendChild(p);

    if (!isUser) {
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);
    } else {
        messageDiv.appendChild(contentDiv);
        // User avatar is hidden via CSS, but structure remains consistent if we want to show it later
    }

    chatBox.appendChild(messageDiv);
    scrollToBottom();
}

// Show typing indicator
function showTyping() {
    const id = 'typing-' + Date.now();
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.id = id;

    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'avatar';
    avatarDiv.textContent = 'IA';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.style.fontStyle = 'italic';
    contentDiv.style.opacity = '0.7';
    contentDiv.textContent = 'Typing...';

    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);

    chatBox.appendChild(messageDiv);
    scrollToBottom();
    return id;
}

function removeTyping(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

// Handle form submission
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    // Add user message
    addMessage(message, true);
    userInput.value = '';

    // Show typing indicator
    const typingId = showTyping();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        // Simulate a small delay for "natural" feel if response is too fast
        setTimeout(() => {
            removeTyping(typingId);
            addMessage(data.response);
        }, 600);

    } catch (error) {
        removeTyping(typingId);
        addMessage("Sorry, I'm having trouble connecting to the server.");
        console.error('Error:', error);
    }
});
