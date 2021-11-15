from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def serialize(self):
        return {
            "id": self.id,
            "user": self.username,
            
        }

class Comments (models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    comment = models.CharField(max_length=510)
    comment_time = models.DateTimeField()
    likes = models.ManyToManyField(User, blank=True, related_name="all_liked_post")
    number_of_likes = models.IntegerField()

    def __str__(self):
        return f" ({self.user_id} {self.comment} {self.comment_time} {self.likes.count() } {self.number_of_likes})"

    def serialize(self):
        return {
            "id": self.id,
            "comment": self.comment,
            "comment_time": self.comment_time,
            "likes": self.likes.count()
        }

class Followers (models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="followers")

    def __str__(self):
        return f" ({self.user_id} {self.follower})"