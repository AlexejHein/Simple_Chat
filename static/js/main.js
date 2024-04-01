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

