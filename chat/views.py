from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .models import Message, Chat


@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        print(request.POST.get('textmessage'))
        myChat = Chat.objects.get(id=1)
        Message.objects.create(text=request.POST.get('textmessage'), chat=myChat,
                               author=request.user, receiver=request.user)
    chatMessages = Message.objects.all()
    return render(request, 'chat/index.html', {'messages': chatMessages})


def login_view(request):
    redirect = request.GET.get('next')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return HttpResponseRedirect(request.POST.get('redirect'))
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
    return render(request, 'auth/login.html', {'redirect': redirect})
