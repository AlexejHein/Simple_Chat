from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Message, Chat


@login_required(login_url='/login/')
def index(request):
    """
    View function to display the chat index page.
    It requires the user to be logged in. If a POST request is received,
    it processes and saves the new message from the user in the chat.
    """
    if request.method == 'POST':
        print(request.POST.get('textmessage'))
        myChat = Chat.objects.get(id=1)
        Message.objects.create(text=request.POST.get('textmessage'), chat=myChat,
                               author=request.user, receiver=request.user)
    chatMessages = Message.objects.all()
    return render(request, 'chat/index.html', {'messages': chatMessages})


def users_view(request):
    """
    View function to display all registered users.
    """
    users = User.objects.all()
    return render(request, 'base.html', {'users': users})


def login_view(request):
    """
    View function for handling user login.
    If the method is POST, it tries to authenticate the user.
    On success, the user is logged in and redirected;
    on failure, it displays the login page again with an error message.
    """
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
    """
    View function for handling new user registration using Django's UserCreationForm.
    If the form is valid, it creates a new user and logs them in.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password2 and password1 != password2:
            return render(request, 'auth/signup.html', {'form': form, 'error': 'The passwords do not match.'})
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})


def logout_view(request):
    """
    View function to logout a user and redirect them to the login page.
    """
    logout(request)
    return redirect('/login/')


def get_messages(request):
    """
    View function to fetch the latest 50 messages if the user is authenticated.
    It returns a JsonResponse containing the messages data or an error if unauthorized.
    """
    if request.user.is_authenticated:
        messages = Message.objects.all().order_by('-created_at')[:50]
        messages_data = [{
            'id': message.id,
            'text': message.text,
            'author': message.author.username,
            'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Sekunden hinzugefügt
        } for message in messages]

        return JsonResponse({'messages': messages_data})

    else:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
