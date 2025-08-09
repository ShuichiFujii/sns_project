from django.contrib import admin
from .models import Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """SNS アプリの投稿モデル

    Args:
        name (Tag): タグの名前
    """
    
    list_display = ('name', )