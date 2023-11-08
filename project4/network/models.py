from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='user_followers')
    following = models.ManyToManyField('self', symmetrical=False, related_name='user_following')
    likes =  models.ManyToManyField('Post', related_name='liked_users', blank=True)

class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    post_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name = 'liked_posts', blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "post_content": self.post_content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": [user.username for user in self.likes.all()],
            "likes_count": self.likes.count(),
        }

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post_content']

