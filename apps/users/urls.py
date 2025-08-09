from django.urls import path, include
from . import views
from apps.posts import views as post_views

app_name = "users"

urlpatterns = [
    # --------------- プロフィール ---------------
    # /<username>/            → 投稿タブ
    # /<username>/posts/      → （同じく）投稿タブ
    path("", views.profile_posts_default,  name="profile_posts_default"),
    path("posts/", views.profile_posts,  name="profile_posts"),

    # /<username>/likes/      → いいねタブ
    path("likes/", views.profile_likes,  name="profile_likes"),

    # /<username>/pins/       → ピン留めタブ（実装済みなら）
    path("pins/",  views.profile_pins,   name="profile_pins"),

    # --------------- 投稿詳細 ---------------
    # /<username>/status/<post_id>/       → posts アプリの再利用
    path("status/<int:post_id>/", post_views.post_detail, name="post_detail"),
    
]