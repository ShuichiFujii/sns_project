from django.contrib import admin
from .models import Like, CommentLike
# Register your models here.

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """SNS アプリの投稿モデル

    Args:
        name (Like): タグの名前
    """
    
    list_display = ('user', 'post', 'created_at')
    
    
@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'created_at')