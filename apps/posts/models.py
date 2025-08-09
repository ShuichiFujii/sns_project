from django.db import models
from django.contrib.auth.models import User
# from apps.tags.models import Tag
from apps.pins.models import Pin

class Post(models.Model):
    """SNS アプリの投稿モデル

    Args:
        author (User): 投稿者
        content (str): 投稿の中身
        tags (Tag): 投稿につけられているタグ
        created_at (datetime): 投稿時間
        views (Int): 投稿の閲覧数
    """
    
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='posts'
    )
    content = models.TextField(max_length=140)
    tags = models.ManyToManyField('tags.Tag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f'{self.author.username}: \n  {self.content[:30]} (at {self.created_at})'
    
    class Meta:
        ordering = ['-created_at']
    
    def toggle_like_by(self, user):
        from apps.likes.models import Like
        like = Like.objects.filter(user=user, post=self).first()

        if like:
            like.delete()
        else:
            Like.objects.create(user=user, post=self)

    def toggle_pin_by(self, user):
        pin = Pin.objects.filter(user=user, post=self).first()

        if pin:
            pin.delete()
        else:
            Pin.objects.create(user=user, post=self)
            
    def get_view_count(self):
        return self.views
            
    def is_liked_by(self, user):
        return self.likes.filter(user=user).exists()
    
    @classmethod
    def get_posts_by_tag(cls, tag):
        return cls.objects.filter(tags=tag)
    
    @classmethod
    def get_posts(cls, user=None):
        if user:
            return cls.objects.filter(author=user)
        return cls.objects.all()
