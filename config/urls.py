from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(redirect_authenticated_user=True, template_name='apps/user/login.html'), name='login'), 
    path('logout/', LogoutView.as_view(), name='logout'), 

    # 投稿タイムライン & CRUD
    path('', include(('apps.posts.urls', 'posts'), namespace='posts')),  

    # 動的ユーザールートは最後に！
    path('<str:username>/', include(('apps.users.urls', 'users'), namespace='users')),

    # 一般的な likes API
    path('likes/', include(('apps.likes.urls', 'likes'), namespace='likes')),
    path('pins/', include(('apps.pins.urls', 'pins'), namespace='pins')),
    
    # # 個人ページ
    # path('<str:username>/likes', views.my_likes, name='my_likes'), 
    path('comments/', include(('apps.comments.urls', 'comments'), namespace='comments')), 
]