from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """SNS アプリの投稿モデル

    Args:
        author (User): 投稿者
        content (str): 投稿の中身
        tags (Tag): 投稿につけられているタグ
        created_at (datetime): 投稿時間
        views (Int): 投稿の閲覧数
    """
    
    list_display = ('author', 'content', 'created_at', 'views')