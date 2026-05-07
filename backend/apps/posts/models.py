from django.db import models
from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True, default='')
    tags = models.TextField(blank=True, default='[]')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'posts_post'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author.username} - {self.created_at}'


class Media(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media', null=True, blank=True)
    file = models.FileField(upload_to='uploads/%Y/%m/')
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPES)
    thumbnail = models.ImageField(upload_to='thumbnails/%Y/%m/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'posts_media'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f'{self.media_type}: {self.file.name}'


class Milestone(models.Model):
    MILESTONE_TYPES = [
        ('roll_over', '翻身'),
        ('sit', '坐'),
        ('crawl', '爬'),
        ('walk', '走路'),
        ('speak', '说话'),
        ('tooth', '长牙'),
        ('wean', '断奶'),
        ('kindergarten', '上幼儿园'),
        ('other', '其他'),
    ]
    baby = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='milestones')
    milestone_type = models.CharField(max_length=20, choices=MILESTONE_TYPES)
    achieved_date = models.DateField()
    description = models.TextField(blank=True, default='')
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True, related_name='milestone_link')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'posts_milestone'
        ordering = ['-achieved_date']

    def __str__(self):
        return f'{self.get_milestone_type_display()} - {self.achieved_date}'
