from django.urls import path
from . import views

app_name = 'posts'          # ← reverse('posts:post_list') 用
urlpatterns = [
    # タイムライン
    path('', views.post_list, name='post_list'), 
    path('home/', views.post_list,   name='post_list'),
    path('create/', views.create_post, name='post_create'),


    # 投稿詳細・編集
    path('<str:username>/detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('<str:username>/<int:post_id>/edit/', views.edit_post,   name='post_edit'),
    path('<str:username>/<int:post_id>/delete/', views.delete_post, name='post_delete')
]
