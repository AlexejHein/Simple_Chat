from datetime import date
from django.conf import settings
from django.db.models.fields import DateField
from django.db import models


class Message(models.Model):
    text = models.CharField(max_length=500)
    created_at = DateField(default=date.today)
    # chat = Chat class
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_messages_set')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='receiver_messages_set')
