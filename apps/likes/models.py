from django.db import models
from django.contrib.auth.models import User
# from apps.posts.models import Post
# from apps.comments.models import Comment

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user}:\n {self.post} (at {self.created_at})'
    
    class Meta:
        # Meta 情報で、Like モデルに制約を課す。
        # user - post の組み合わせは一意である。
        unique_together = ('user', 'post')
        
class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
    comment = models.ForeignKey('comments.Comment', on_delete=models.CASCADE, related_name='comment_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user}:\n {self.comment} (at {self.created_at})'
    
    class Meta:
        unique_together = ('user', 'comment')
        