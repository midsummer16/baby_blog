from django.db import models
from django.conf import settings


class Comment(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'social_comment'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author.username}: {self.content[:20]}'


class Like(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'social_like'
        unique_together = ['post', 'user']

    def __str__(self):
        return f'{self.user.username} likes {self.post.id}'


class Blessing(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='blessings')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'social_blessing'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author.username}: {self.content[:20]}'
