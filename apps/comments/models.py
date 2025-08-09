from django.db import models
from apps.posts.models import Post
# from apps.tags.models import Tag
# from apps.likes.models import Like
from django.contrib.auth.models import User

class Comment(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    # created_at = models.DateTimeField() # テスト用
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.id}'
    
    @classmethod
    def get_comments(cls, post_id):
        return cls.objects.filter(post__id=post_id).order_by('-created_at', '-pk')