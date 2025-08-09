from django.db import models
from django.contrib.auth.models import User
    
class Pin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pins')
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='pins')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')
        