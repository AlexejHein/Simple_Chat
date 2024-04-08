from django.contrib.auth.models import User


def users(request):
    return {'users': User.objects.all()}
