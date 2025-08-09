from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from apps.posts.models import Post
from apps.likes.models import Like
from django.contrib.auth import get_user_model
from apps.comments.models import Comment
from apps.tags.models import Tag

@login_required
def post_pin_toggle(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.toggle_pin_by(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'post_list'))

