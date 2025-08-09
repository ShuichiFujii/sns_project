from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from apps.posts.models import Post
from apps.tags.models import Tag
from apps.comments.models import Comment
from django.contrib.auth.models import User

# from django.views.generic import ListView


@login_required
def post_detail(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.get_comments(post_id)
    tags = post.tags.all().order_by('name')
    post.views += 1
    
    print(f"🔥View: {post.views}")
    for comment in comments:
        comment.liked_by_me = comment.comment_likes.filter(user=request.user).exists()
    
    post.save()
    return render(request, 'apps/post/detail.html', {'comments': comments, 'post': post, 'tags': tags})


@login_required
def create_post(request):
    error = None
    content = ""
    tags = ""
    
    if request.method == 'POST': # 投稿フォームを押したとき
        content = request.POST.get('content')
        tags = request.POST.get('tags', '')
        
        print("🔥 投稿フォームから受け取った tags:", tags)  # これを追加！
        
        if content:
            post = Post.objects.create(author=request.user, content=content)
            
            tag_list = [name.strip() for name in tags.split(',') if name.strip()]
            
            for name in tag_list:
                tag, _ = Tag.objects.get_or_create(name=name)
                post.tags.add(tag)
                
            return redirect('posts:post_list')
        else:
            error = '本文を入力してください。'
    
    # 最初のアクセス、フォームを表示するだけ（GET）
    return render(request, 'apps/post/create.html', {'content': content, 'error': error, 'tags': tags}) # 初回アクセス時

@login_required
def edit_post(request, username, post_id):
    post = Post.objects.get(pk=post_id)
    tags_input = ', '.join([tag.name for tag in post.tags.all()])
    error = None
    
    if request.method == 'POST': # 編集ボタンを押したとき
        content = request.POST.get('content')
        tags = request.POST.get('tags', '')
        
        if content:
            post.content = request.POST.get('content')
            post.save()
            
            # タグ処理をリセットして上書き
            tag_list = [name.strip() for name in tags.split(',') if name.strip()]
            tag_objs = []

            for name in tag_list:
                tag, _ = Tag.objects.get_or_create(name=name)
                tag_objs.append(tag)

            post.tags.set(tag_objs)  # ← setでリセット＆追加

            return redirect('posts:post_list')
        else:
            error = '本文を入力してください'
            
    return render(request, 'apps/post/edit.html', {'post': post, 'error': error, 'tags': tags_input})

@login_required
def delete_post(request, username, post_id):
    post = Post.objects.filter(pk=post_id, author=request.user)
    
    if request.method == 'POST':
        # post を削除する
        post.delete()
        return redirect('my_posts')
    
    return render(request, 'apps/post/list.html', {'view_mode': 'mine'})

@login_required
def post_list(request):
    posts = Post.get_posts()
    
    for post in posts:
        post.liked_by_me = post.is_liked_by(request.user) # テンプレートに渡す
        
    return render(request, 'apps/post/list.html', {'posts': posts})
