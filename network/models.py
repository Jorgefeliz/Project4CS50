from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Comments (models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_items")
    comment = models.CharField(max_length=510)
    comment_time = models.DateTimeField()

    def __str__(self):
        return f" ({self.user_id} {self.comment} {self.comment_time})"

