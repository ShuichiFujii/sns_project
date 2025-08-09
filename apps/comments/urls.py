from django.urls import path
from . import views

app_name = 'comments'          # ← reverse('posts:post_list') 用

urlpatterns = [
    path('posts/<int:post_id>/comment/', views.create_comment, name='comment_create'),
]
