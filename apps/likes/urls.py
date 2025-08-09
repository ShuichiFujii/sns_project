# apps/likes/urls.py
from django.urls import path
from . import views

app_name = 'likes'

urlpatterns = [
    # path('<str:username>/likes/', views.my_likes, name='my_likes'),
    path('<int:post_id>/toggle/', views.post_like_toggle, name='post_like_toggle'),
]
