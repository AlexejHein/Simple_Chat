window.onload = function() {
    let chatContent = document.querySelector('.chat-content');
    chatContent.scrollTop = chatContent.scrollHeight;
}

function scroll(){
    let chatContent = document.querySelector('.chat-content');
    chatContent.scrollTop = 0;
}