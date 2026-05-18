from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)

    def __str__(self):
        return self.user.username
    

class Notification(models.Model):
    # Mapping numbers to specific notification types
    NOTIFICATION_TYPES = ((1, 'Like'), (2, 'Comment'), (3, 'Follow'))
    
    # The user receiving the notification
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    # The user who triggered the action
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_notifications')
    
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, blank=True, null=True)
    text_preview = models.CharField(max_length=90, blank=True) # To show a snippet of the comment
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} -> {self.user} ({self.notification_type})"    
