document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('sendMessageForm');
    form.addEventListener('submit', sendMessage);

    loadMessages().then(r => {});
});


async function loadMessages() {
    let currentUsername = document.getElementById('currentUsername').innerText;
    console.log(currentUsername);
    try {
        const response = await fetch('/chat/get_messages/');
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        const data = await response.json();
        const messagesContainer = document.getElementById('messages');
        messagesContainer.innerHTML = '';
        data.messages.forEach(message => {
            const messageElement = document.createElement('div');
            messageElement.className = 'chat-box';
            // Add class based on author
            if (message.author === currentUsername) {
                messageElement.classList.add('own-message');
            } else {
                messageElement.classList.add('other-message');
            }
            const createdAt = new Date(message.created_at).toLocaleString();
            messageElement.innerHTML = `<small class="color-gray">${createdAt} ${message.author}:</small><br><i>${message.text}</i>`;
            messagesContainer.appendChild(messageElement);
        });
    } catch (error) {
        console.error('Failed to load messages:', error);
    }
}


async function sendMessage(event) {
    event.preventDefault();
    const form = document.getElementById('sendMessageForm');
    const messageField = document.getElementById('messageField');
    const text = messageField.value;
    const messageDisplay = document.createElement('div');
    messageDisplay.className = 'chat-box temp-message';
    messageDisplay.innerHTML = `<small class="color-gray">${new Date().toLocaleTimeString()} Me:</small><br>${text}`;
    document.getElementById('messages').appendChild(messageDisplay);
    scrollToEnd();

    const fd = new FormData(form);
    fd.append('textmessage', text);
    fetch('/chat/', {
        method: 'POST',
        body: fd
    }).then(response => {
        if (response.ok) {
            messageDisplay.classList.remove('temp-message');
        } else {
            messageDisplay.classList.add('error-message');
        }
        messageField.value = '';
    }).catch(error => {
        console.error('Error sending message', error);
        messageDisplay.classList.add('error-message');
    });
}


function scrollToEnd() {
    const chatContent = document.querySelector('.chat-content');
    if (chatContent) {
        chatContent.scrollTop = chatContent.scrollHeight;
    }
}