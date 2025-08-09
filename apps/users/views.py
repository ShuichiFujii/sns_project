from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from apps.posts.models import Post
User = get_user_model()

# 共通ユーティリティ -------------------------------------------------
def _annotate_like_flags(posts, viewer):
    """各 Post に liked_by_me フラグを付与"""
    for p in posts:
        p.liked_by_me = p.is_liked_by(viewer)
    return posts

# ビュー内でリダイレクト
def profile_posts_default(request, username):
    return redirect("users:profile_posts", username=username)

# ---------------- 投稿タブ ----------------
@login_required
def profile_posts(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = _annotate_like_flags(Post.get_posts(user=profile_user), request.user)

    ctx = {
        "profile_user": profile_user,
        "posts": posts,
        "posts_count": posts.count(),
        "likes_count": profile_user.likes.count(),
        "active_tab": "posts",
    }
    return render(request, "apps/user/profile/tab_posts.html", ctx)

# ---------------- いいねタブ ----------------
@login_required
def profile_likes(request, username):
    profile_user = get_object_or_404(User, username=username)
    liked_posts = _annotate_like_flags(
        Post.objects.filter(likes__user=profile_user).select_related("author").order_by("-created_at"),
        request.user,
    )

    ctx = {
        "profile_user": profile_user,
        "liked_posts": liked_posts,
        "likes_count": liked_posts.count(),
        "posts_count": profile_user.posts.count(),
        "active_tab": "likes",
    }
    return render(request, "apps/user/profile/tab_likes.html", ctx)

# ---------------- ピン留めタブ（任意） ----------------
@login_required
def profile_pins(request, username):
    # 実装済みなら Pin モデルで取得
    return render(request, "apps/user/profile/tab_pins.html", {
        # 実装例： "pinned_posts": pinned_posts, ...
    })
