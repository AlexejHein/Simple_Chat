window.onload = function() {
    setTimeout(scrollToEnd, 100);
}

function scrollToEnd() {
    let chatContent = document.querySelector('.chat-content');
    if (chatContent) {
        chatContent.scrollTop = chatContent.scrollHeight;
    }
}

document.querySelector('.sand-box form').addEventListener('submit', function(event) {
    setTimeout(scrollToEnd, 10);
});

window.sendMessage = async function() {
    let messageField = document.getElementById('messageField');
    let fd = new FormData();
    let token = '{{ csrf_token }}';
    fd.append('textmessage', messageField.value);
    fd.append('csrfmiddlewaretoken', token);
    try {
        await fetch('/chat/', {
                method: 'POST',
                body: fd
            }).then(r => {
                console.log('Message sent');
        });

    } catch (e) {
        console.error('Error sending message');
    }
}