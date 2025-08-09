from django.contrib import admin
from .models import Pin

@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    """SNS アプリの投稿モデル

    Args:
        name (Pin): タグの名前
    """
    
    list_display = ('user', 'post', 'created_at')