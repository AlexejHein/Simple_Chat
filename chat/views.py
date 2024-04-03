from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
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
    redirect = request.GET.get('next', '/')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return HttpResponseRedirect(request.POST.get('redirect'))
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
    return render(request, 'auth/login.html', {'redirect': redirect})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/login/')


def get_messages(request):
    if request.user.is_authenticated:
        messages = Message.objects.all().order_by('-created_at')[:50]
        messages_data = [{
            'id': message.id,
            'text': message.text,
            'author': message.author.username,
            'created_at': message.created_at.strftime('%Y-%m-%d %H:%M')
        } for message in messages]

        return JsonResponse({'messages': messages_data})

    else:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
