from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.posts.models import Post
from apps.tags.models import Tag
from apps.likes.models import Like
from apps.comments.models import Comment
from django.utils import timezone

def create_user(client, username, password='password1234'):
    new_user = User.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    return new_user

def create_post(author, content):
    return Post.objects.create(author=author, content=content)

def create_comment(author, post, comment, created_at=None):
    return Comment.objects.create(author=author, post=post, comment=comment, created_at=created_at or timezone.now())
    
class CommentViewTests(TestCase):        
    def test_create_comment(self):
        self.client = Client()
        
        post_author = create_user(self.client, 'author')
        post = create_post(post_author, '投稿内容')
        
        referrer_url = reverse('posts:post_detail', kwargs={'username': post_author.username, 'post_id': post.id})
        
        comments = ['comment1', 'comment2', 'comment3']
        
        for comment in comments:
            response = self.client.post(
                reverse('comments:comment_create', kwargs={'post_id': post.id}), 
                data={'comment': comment}, 
                HTTP_REFERER=referrer_url
            )
        
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, referrer_url)
            self.assertTrue(Comment.objects.filter(post=post, comment=comment, author=post_author).exists())

class CommentModelTests(TestCase):    
    def test_get_comments(self):
        self.client = Client()
        
        user1 = create_user(self.client, 'Tom')
        user2 = create_user(self.client, 'Alice')
        user3 = create_user(self.client, 'Kim')
        post  = create_post(user1, 'Hello!')

        # コメントを「作成順」に作る
        create_comment(user2, post, 'First')
        create_comment(user3, post, 'Second')
        create_comment(user3, post, 'Third')

        # get_comments は created_at 降順なので、
        # 最後に作った Third → Second → First の順で返るはず
        comments = Comment.get_comments(post.id)
        self.assertEqual(comments.count(), 3)
        
        authors = [c.author for c in comments]
        self.assertEqual(authors, [user3, user3, user2])