// This function initializes the form and message loading once the DOM content is fully loaded.
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById('sendMessageForm');
    form.addEventListener('submit', sendMessage);
    loadMessages().then(r => scrollToEnd());
});


// Asynchronously load messages from the server and display them.
async function loadMessages() {
    const currentUsername = document.getElementById('currentUsername').innerText;
    try {
        const response = await fetch('/chat/get_messages/');
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        const { messages } = await response.json();
        const messagesContainer = document.getElementById('messages');
        messagesContainer.innerHTML = ''; // Clear existing messages before loading new ones
        messages.forEach(message => {
            const messageElement = createMessageElement(message, currentUsername);
            messagesContainer.appendChild(messageElement); 
        });
    } catch (error) {
        console.error('Failed to load messages:', error);
    }
}


// Creates a message element for display in the chat window.
function createMessageElement(message, currentUsername) {
    const messageElement = document.createElement('div');
    messageElement.className = `chat-box ${message.author === currentUsername ? 'own-message' : 'other-message'}`;
    const createdAt = new Date(message.created_at).toLocaleString('de-DE', {
        year: 'numeric', month: '2-digit', day: '2-digit', 
        hour: '2-digit', minute: '2-digit', second: '2-digit'
    });
    messageElement.innerHTML = `<small class="color-gray">${createdAt}<span class="autorName"> ${message.author} </span> :</small><br>${message.text}`;
    return messageElement;
}


// Initializes and displays the message in the chat before sending
function prepareMessageDisplay(currentUsername, text) {
    const messageDisplay = createTempMessageDisplay(currentUsername, text);
    document.getElementById('messages').appendChild(messageDisplay);
    scrollToEnd();
    return messageDisplay;
}

// Sends the message to the server and handles the response
async function sendMessageToServer(form, text, messageDisplay) {
    const fd = new FormData(form);
    fd.append('textmessage', text);
    try {
        const response = await fetch('/chat/', { method: 'POST', body: fd });
        await handleServerResponse(response, messageDisplay);
    } catch (error) {
        console.error('Error sending message', error);
        messageDisplay.classList.add('error-message');
    }
}

// Handles the server response after sending a message
async function handleServerResponse(response, messageDisplay) {
    if (response.ok) {
        messageDisplay.classList.remove('temp-message');
        await loadMessages(); // Reload messages to include the new one
    } else {
        messageDisplay.classList.add('error-message');
    }
}

// Main function to handle the send message event
async function sendMessage(event) {
    event.preventDefault();
    const currentUsername = document.getElementById('currentUsername').innerText;
    const form = document.getElementById('sendMessageForm');
    const messageField = document.getElementById('messageField');
    const text = messageField.value;

    const messageDisplay = prepareMessageDisplay(currentUsername, text);
    await sendMessageToServer(form, text, messageDisplay);

    messageField.value = ''; // Clear the message field after sending
}


// Creates a temporary message display element in the chat window.
function createTempMessageDisplay(username, text) {
    const messageDisplay = document.createElement('div');
    messageDisplay.className = 'chat-box temp-message';
    messageDisplay.innerHTML = `<small class="color-gray">${new Date().toLocaleTimeString()} ${username}</small><br>${text}`;
    return messageDisplay;
}

// Scrolls the chat content to the end to show the most recent messages.
function scrollToEnd() {
    const chatContent = document.querySelector('.chat-content');
    if (chatContent) {
        chatContent.scrollTop = chatContent.scrollHeight;
    }
}
