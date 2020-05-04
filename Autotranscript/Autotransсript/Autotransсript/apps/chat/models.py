from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Message(models.Model):
    author = models.ForeignKey(User, related_name = 'author_messages', on_delete = models.CASCADE)
    content = models.TextField()
    chat = models.CharField(max_length = 50)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.author.username
    def last_20_messeges(self):
        return Message.objects.order_by('-timestamp').all()[:20]
