from django.shortcuts import render

from .models import Message, Chat


def index(request):
    if request.method == 'POST':
        print(request.POST.get('textmessage'))
        myChat = Chat.objects.get(id=1)
        Message.objects.create(text=request.POST.get('textmessage'), chat=myChat,
                               author=request.user, receiver=request.user)
    chatMessages = Message.objects.all()
    return render(request, 'chat/index.html', {'messages': chatMessages})
