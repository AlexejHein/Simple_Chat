from django.shortcuts import render


def index(request):
    if request.method == 'POST':
        print(request.POST.get('textmessage'))
    return render(request, 'chat/index.html', {})
