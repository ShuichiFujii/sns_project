from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from apps.posts.models import Post
from apps.tags.models import Tag
from apps.likes.models import Like
from apps.comments.models import Comment
from apps.tags.models import Tag

@login_required
def create_comment(request, post_id):
    error = None
    comment = ""
    
    if request.method == 'POST':
        comment = request.POST.get('comment')
        
        if comment:
            post = get_object_or_404(Post, pk=post_id)
            Comment.objects.create(author=request.user, comment=comment, post=post)
            return redirect('posts:post_detail', username=post.author.username, post_id=post_id)
        else:
            error = '本文を入力してください'
            
    return redirect(request.META.get('HTTP_REFERER'))