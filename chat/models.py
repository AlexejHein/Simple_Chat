from datetime import date
from django.conf import settings
from django.db import models


class Chat(models.Model):
    # users = models.ManyToManyField(User)
    # messages = models.ManyToManyField(Message)
    created_at = models.DateField(default=date.today)


class Message(models.Model):
    text = models.CharField(max_length=500)
    created_at = models.DateField(default=date.today)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_messages_set',
                             default=None, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_messages_set')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='receiver_messages_set')
